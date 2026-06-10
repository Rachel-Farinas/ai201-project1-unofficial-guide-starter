# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---
This system covers student reviews and feedback of CS professors at the University of Miami. 
This is relevant because many students aren't familiar with professors' teaching style and may
not personally know anyone who has experience with a certain professor. This system helps bridge that gap by addressing questions on teaching style, exam style, workload, and textbook relevance.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

Sources include 178 professor CSV files, with each file containing Rate My Professor reviews for that professor and corresponding metadata (Date, Quality, Difficulty, Tags, Course, For Credit, Attendance, Grade, Textbook, Thumbs Up, Thumbs Down). 

Also includes a list of all professors scraped and their metadata (Name, Department, Overall Rating, Number of Ratings, Would Take Again Percent, Level of Difficulty).

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | A Fahad_reviews.csv | CSV | ./professor_reviews/documents |
| 2 | Abdul Hamid Samra_reviews.csv | CSV | ./professor_reviews/documents |
| 3 | Akmal Younis_reviews.csv | CSV | ./professor_reviews/documents |
| 4 | Alan Lazer_reviews.csv | CSV | ./professor_reviews/documents |
| 5 | Alexander Korogodsky_reviews.csv | CSV | ./professor_reviews/documents |
...
| 178 | Zheng Wang_reviews.csv | CSV | ./professor_reviews/documents |
| 179 | professors_list.csv | CSV | ./documents |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** MAX_CHARS = 1000

**Overlap:** OVERLAP_CHARs = 200

**Reasoning:** Each RMP review is a short, self-contained comment that fits well within 1000 characters alongside its metadata (course, grade, tags). The 200-character overlap is a conservative safeguard for longer reviews that may get split at a boundary, ensuring no context is lost at the cut point.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast and runs locally but has a 256-token context window and was trained on general text, so it may underperform on academic phrasing like "easy grader" or course codes. In production the main tradeoffs would be accuracy on domain-specific text (a model fine-tuned on review-style text would produce better semantic matches), context length (models like text-embedding-3-small support up to 8191 tokens, eliminating most chunking concerns), and latency vs. accuracy. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Dilip Sarkar's difficulty? | Students consistently describe Sarkar as tough/difficult, recommend the textbook and outside resources |
| 2 | Would students recommend taking David Chapman? | Yes, reviews describe him as caring and a good lecturer |
| 3 | How do students rate Geoff Sutcliffe's workload? | References to homework load and assignment frequency from his reviews |
| 4 | Who is easier, Dilip Sarkar or Blake Rosenberg? | Direct comparison based on difficulty ratings and review comments |
| 5 | Does Odelia Schwartz have reviews mentioning exams? | System should return relevant review excerpts or say not enough information if none mention exams |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Short or vague reviews: many RMP comments are 1-2 sentences with little substance (e.g. "great professor"), which may retrieve as top results but not actually answer the query, producing low-quality responses.

2. Professor name mismatches: if a user queries "Sarkar" instead of "Dilip Sarkar", the retriever may fail to match the chunk metadata, returning no results even when relevant reviews exist.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


| Stage | Tool | Input | Expected output | Verification |
|-------|------|-------|-----------------|--------------|
| Chunking | Claude | Chunking Strategy section + current `ingest.py` | `chunk_text()` implementing 1000-char chunks with 200-char overlap | Manually check chunk boundaries on a known review |
| Embedding + Vector Store | Claude | Architecture section + ChromaDB docs | `embed_and_store()` using `all-MiniLM-L6-v2` and ChromaDB | Query store and confirm reviews are returned |
| Retrieval | Claude | Retrieval Approach section | `retrieve()` returning top-k chunks with metadata | Run evaluation plan questions and check sources cited |
| Generation | Claude | System prompt + Grounded Generation section | `generate()` wrapping Groq call with context injection | Confirm model cites `[1]`-style sources and refuses out-of-scope questions |
