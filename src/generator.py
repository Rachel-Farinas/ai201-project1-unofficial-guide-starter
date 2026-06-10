import os
from groq import Groq
from config import LLM_MODEL


# Create the Groq client once, at module load, so every call reuses it.
# (config.py already called load_dotenv(), so GROQ_API_KEY is in the environment.)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_context(chunks):
    """Turn the retrieved chunks into one readable text block to feed the LLM.

    `chunks` is the list your retriever returns — each item has the nested
    shape you built in ingest.py: chunk["Professor"]["Name"] and
    chunk["Review"]["Comment"], plus the metadata dicts.
    """

    # 1. Create an empty list `lines` (you'll join it into one string at the end).
    lines = []

    # 2. Loop over each chunk (use enumerate so you can number the sources, e.g. [1], [2]).
    for index, chunk in enumerate(chunks, start=1):

        # chunks from retrieve() are flat: {id, text, metadata}
        chunk_id = chunk["id"]
        review = chunk["text"]
        meta = chunk["metadata"]

        name = meta.get("professor", "")
        overall_rating = meta.get("overall rating", "")
        overall_difficulty = meta.get("overall difficulty", "")
        number_of_ratings = meta.get("number of ratings", "")
        would_take_again = meta.get("would take again", "")
        quality = meta.get("quality", "")
        reviewer_difficulty = meta.get("reviewer difficulty", "")
        course = meta.get("course", "")
        textbook = meta.get("textbook", "")

        heading = f"[{index}]\nID: {chunk_id} Professor: {name}\n"
        professor_metadata = f"Course: {course}\nOverall Rating: {overall_rating}\nNumber of Ratings: {number_of_ratings}\nWould Take Again percent: {would_take_again}\nLevel of Difficulty: {overall_difficulty}\n"
        review_metadata = f"Quality: {quality}\nReviewer Difficulty: {reviewer_difficulty}\nTextbook: {textbook}\n"
        review_text = f"Text: {review}"

        lines.append(heading + professor_metadata + review_metadata + review_text)

    # 3. Join `lines` into one big string and return it.
    return "\n\n".join(lines)

def build_messages(query, context):
    """Build the chat messages list for the LLM (a system message + a user message)."""

    # 1. Write a SYSTEM message that sets the rules, e.g.:
    #    - "You answer questions about professors using ONLY the reviews provided."
    #    - "If the context doesn't contain the answer, say you don't know."
    #    - "Cite the sources you use by their [number]."

    system = """
    
    You are an advisor that provides advice about which University of Miami professors 
    to take using Rate My Professor reviews.\n

    Rules:
    - Do not use outside information. Only use the information provided to answer questions.\n
    - If the context doesn't contain the answer, say you don't have enough information to answer.\n
    - Do not guess an answer if you don't have enough context.\n
    - Cite the sources you use by their number (e.g., [1]).\n
    - Be concise and base every claim on the reviews.\n
    - If a user asks to compare two professors and one professor has no reviews,
      say you don't have enough information to answer.\n
    - 
    """

    # 2. Write a USER message that contains BOTH the context and the question, e.g.:
    #    f"Context:\n{context}\n\nQuestion: {query}"
    user = f"""Context:\n

    {context}\n\n
    Question: {query}

    """

    return[
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]


def generate_answer(query, chunks):
    """Top-level entry point: question + retrieved chunks -> generated answer string."""

    # 1. Turn the chunks into a context string:   context = format_context(chunks)
    context = format_context(chunks)

    # 2. Build the messages:                       messages = build_messages(query, context)
    messages = build_messages(query, context)

    # 3. Call the LLM through the Groq client:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2,   # low (e.g. 0.2) keeps answers grounded in the context
    )

    # 4. Pull the text out of the response:
    answer = response.choices[0].message.content

    # 5. Return `answer`.
    return answer
