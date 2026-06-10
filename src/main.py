from ingest import load_documents, chunk_data
from retriever import get_collection, index_chunks, retrieve
from generator import generate_answer


def build_index():
    """PHASE A — load reviews, chunk them, and store them in Chroma.

    Skips re-indexing if the collection already has data, so startup is fast
    on later runs. (Delete ./chroma_db if you want to force a rebuild.)
    """
    collection = get_collection()
    if collection.count() > 0:
        print(f"Index already has {collection.count()} chunks — skipping ingest.")
        return

    professors = load_documents()
    chunks = chunk_data(professors)
    count = index_chunks(chunks)
    print(f"Indexed {count} chunks.")


def answer_question(query):
    """PHASE B — retrieve the most relevant chunks and generate an answer."""
    hits = retrieve(query)
    return generate_answer(query, hits)


def main():
    # Phase A: make sure the vector store is populated.
    build_index()

    # Phase B: simple question loop (blank line or Ctrl+C to quit).
    print("\nAsk about University of Miami professors. Press Enter on an empty line to quit.")
    while True:
        query = input("\nQuestion: ").strip()
        if not query:
            break
        print(f"\n{answer_question(query)}")


if __name__ == "__main__":
    main()
