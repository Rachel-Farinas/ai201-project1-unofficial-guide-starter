import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_PATH, CHROMA_COLLECTION, EMBEDDING_MODEL, N_RESULTS


def get_collection():
    """Connect to Chroma on disk and return the collection (used by both phases).

    The collection is created with a SentenceTransformer embedding function, so
    Chroma converts text -> embeddings for you automatically on add() and query().
    """

    # 1. Create the embedding function from EMBEDDING_MODEL, e.g.:
    #    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    #        model_name=EMBEDDING_MODEL
    #    )
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    # 2. Create a persistent Chroma client pointed at CHROMA_PATH:
    #    client = chromadb.PersistentClient(path=CHROMA_PATH)
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # 3. Get or create the collection by name (CHROMA_COLLECTION), passing the
    #    embedding function so Chroma embeds automatically:
    #    collection = client.get_or_create_collection(
    #        name=CHROMA_COLLECTION, embedding_function=embedding_fn
    #    )
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION, embedding_function=embedding_fn
    )

    # 4. Return the collection.

    return collection


def flatten_chunk(chunk):
    """Turn one nested chunk into (id, document_text, flat_metadata) for Chroma.

    Chroma needs the text separate from a FLAT metadata dict whose values are
    only str / int / float / bool — your nested Professor/Review dicts won't work
    as-is, so pick out the fields you want and flatten them here.
    """

    # 1. Pull the id:        chunk["id"]
    chunk_id = chunk["id"]

    # 2. Pull the document text (what gets embedded/searched):
    #    chunk["Review"]["Comment"]
    text = chunk["Review"]["Comment"]

    # 3. Build a FLAT metadata dict (one level deep, scalar values only), e.g.:
    #    {
    #        "professor": chunk["Professor"]["Name"],
    #        "course":    chunk["Review"]["Metadata"].get("Course", ""),
    #        "quality":   chunk["Review"]["Metadata"].get("Quality", ""),
    #        ... any other fields you'll want to filter on or show ...
    #    }

    professor_meta = chunk["Professor"]["Metadata"]
    review_meta = chunk["Review"]["Metadata"]

    metadata = {
        "professor": chunk["Professor"]["Name"],
        "overall rating": professor_meta.get("Overall Rating", ""),
        "overall difficulty": professor_meta.get("Level of Difficulty", ""),
        "number of ratings": professor_meta.get("Number of Ratings", ""),
        "would take again": professor_meta.get("Would Take Again Percent", ""),
        "quality": review_meta.get("Quality", ""),
        "reviewer difficulty": review_meta.get("Difficulty", ""),
        "course": review_meta.get("Course", ""),
        "textbook": review_meta.get("Textbook", ""),
    }

    # 4. Return the three pieces: return id, document_text, metadata

    return chunk_id, text, metadata


def index_chunks(chunks):
    """PHASE A — store all chunks in Chroma (run once, or when documents change)."""

    # 1. Get the collection:   collection = get_collection()
    collection = get_collection()

    # 2. Build three parallel lists by flattening every chunk.
    ids = []
    documents = []
    metadatas = []
    for chunk in chunks:
        chunk_id, text, metadata = flatten_chunk(chunk)
        ids.append(chunk_id)
        documents.append(text)
        metadatas.append(metadata)

    # 3. Add everything to the collection in one call.
    #    upsert (rather than add) overwrites existing ids, so re-running this
    #    function won't error on duplicates. (Chroma embeds the documents for you.)
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    # 4. Return how many chunks you indexed, for a sanity print.
    return len(ids)


def retrieve(query, n_results=N_RESULTS):
    """PHASE B — embed the query and return the top matching chunks for it."""

    # 1. Get the collection.
    collection = get_collection()

    # 2. Query the collection for the most similar documents.
    #    (Chroma embeds `query` with the same model used at index time.)
    results = collection.query(query_texts=[query], n_results=n_results)

    # 3. `results` is a dict of parallel lists keyed by the (single) query.
    #    Grab the lists for our one query (index 0) and zip them into one dict per hit.
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    ids = results["ids"][0]

    hits = []
    for chunk_id, text, metadata in zip(ids, documents, metadatas):
        hits.append({
            "id": chunk_id,
            "text": text,
            "metadata": metadata,
        })

    # 4. Return that list of retrieved chunks.
    return hits
