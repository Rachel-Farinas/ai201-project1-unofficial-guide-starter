# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---
This system covers student reviews and feedback of CS professors at the University of Miami. 
This is relevant because many students aren't familiar with professors' teaching style and may
not personally know anyone who has experience with a certain professor. This system helps bridge that gap by addressing questions on teaching style, exam style, workload, and textbook relevance.

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** Limited to a row in a CSV file (both for professor reviews and professor list).

**Overlap:** No overlap as CSV rows are unrelated to each other and self-contained.

**Why these choices fit your documents:** Every professor's list of reviews and the professor's information
are contained in CSV rows. There is no overlap between pieces of information, so keeping chunking limited
to what is contained in each row makes the most sense here.

**Final chunk count:** 2157

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:**

`all-MiniLM-L6-v2` is fast, runs entirely locally, and requires no API key — ideal for development. Its main limitation is a 256-token context window, which means longer reviews that get split at chunk boundaries lose cross-sentence context at the embedding stage. For production I would weigh three tradeoffs: (1) **accuracy on domain-specific text** — a model fine-tuned on review-style or education text would produce tighter semantic matches for informal phrasing like "easy grader" or "curves a lot," where general-purpose embeddings may miss intent; (2) **context length** — a model like `text-embedding-3-small` (8191-token window) would eliminate most chunking concerns for long reviews; (3) **latency vs. quality** — a hosted API embedding model is slower per query and adds cost, but typically outperforms the local 22 M-parameter MiniLM on recall for nuanced queries. For this corpus of short review comments, MiniLM's 256-token window is rarely the bottleneck, so the main production upgrade would be domain fine-tuning or a larger general-purpose model.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** 

You are an advisor that provides advice about which University of Miami professors 
to take using Rate My Professor reviews.

Rules:
- Do not use outside information. Only use the information provided to answer questions.
- If the context doesn't contain the answer, say you don't have enough information to answer.
- Do not guess an answer if you don't have enough context.
- Cite the sources you use by their number (e.g., [1]).
- Be concise and base every claim on the reviews.
- If a user asks to compare two professors and one professor has no reviews,
  say you don't have enough information to answer.

**How source attribution is surfaced in the response:** The system prompt instructs the model to cite sources by number (e.g., [1]). Each retrieved chunk passed to the model is numbered and includes the professor name and review metadata as context, so when the model makes a claim it can reference the specific review it drew from. This means a response like "Chapman is known for being approachable [1]" traces directly back to a specific numbered review chunk, not a general impression across all retrieved documents. If no relevant chunks are retrieved above the similarity threshold, the model is instructed to explicitly say it doesn't have enough information rather than fall back on general knowledge.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Dilip Sarkar's difficulty? | Students consistently describe Sarkar as tough; difficult tests and arbitrary grading mentioned | Confirmed Sarkar's difficulty rating (4.0–5.0 across chunks), quoted "He is difficult, but the material is not" and "difficult tests" and "arbitrary grading"; cited [1], [4], [5] | Relevant | Accurate |
| 2 | Would students recommend taking David Chapman? | Yes — reviews describe him as caring and a good lecturer | "I don't have enough information to answer. There is no review about David Chapman in the provided context." | Off-target | Inaccurate |
| 3 | How do students rate Geoff Sutcliffe's workload? | References to homework load and assignment frequency | Cited difficulty rating of 3.3 and quoted "The course work is tough, but he makes it feel like its no big deal"; acknowledged Sutcliffe is manageable due to his teaching style | Relevant | Partially accurate |
| 4 | Who is easier, Dilip Sarkar or Blake Rosenberg? | Direct comparison based on difficulty ratings and review comments | "I don't have enough information to answer. There is no review for Blake Rosenberg in the provided context." | Off-target | Accurate (no "Blake Rosenberg" exists in the database; professor is Burton Rosenberg) |
| 5 | Does Odelia Schwartz have reviews mentioning exams? | Return relevant review excerpts or say not enough info if none mention exams | Found and cited a review stating "her exams are easy if you have paid attention in class" | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "Would students recommend taking David Chapman?"

**What the system returned:** "I don't have enough information to answer. There is no review about a professor named David Chapman in the provided context."

**Root cause (tied to a specific pipeline stage):** The failure is in the **Embedding + Retrieval** stage. During indexing, each chunk's embedded text is the review *comment* — the professor's name is stored only in the flat metadata dict, not in the document text that Chroma embeds. When the query "Would students recommend taking David Chapman?" is embedded and compared against stored vectors, the similarity score is computed against comment text like "great lecturer, always available." Because Chapman has only 2 reviews and neither comment contains his name or the word "recommend," those 2 chunks rank outside the top-5 by cosine similarity and are never returned. The model has no Chapman context and correctly says it doesn't know — but the underlying problem is that name-based queries can't be resolved through semantic similarity on comment text alone.

**What you would change to fix it:** Prepend the professor's name to the stored document text at index time (e.g., `"Professor: David Chapman\n" + comment`). This embeds the name into the vector space so that queries containing a professor's name get a direct semantic signal toward that professor's chunks, even when the comments themselves are generic.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The Chunking Strategy section of planning.md specified concrete numbers — MAX_CHARS = 1000 and OVERLAP_CHARS = 200 — which translated directly into constants in `config.py` without any guesswork. Having the reasoning written down ("self-contained review comments, conservative overlap as safeguard for longer reviews") also made it easy to justify keeping each CSV row as a single chunk rather than splitting on arbitrary character counts, since reviews are already short and bounded by the row structure.

**One way your implementation diverged from the spec, and why:** The evaluation plan in planning.md listed "Blake Rosenberg" as a professor for Q4. During testing, the system correctly reported no reviews for Blake Rosenberg — because the database contains "Burton Rosenberg," not "Blake." The name mismatch in the spec was discovered only at evaluation time, which surfaced a broader design issue: the system has no fuzzy name matching. A user who misspells or partially recalls a professor's name will get a "not enough information" response even when that professor's reviews are in the index. The implementation stayed true to exact-name matching at the embedding level, which the spec did not anticipate as a failure mode.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from planning.md and the skeleton of `ingest.py`, asking it to implement `split_text()` and `chunk_data()` using 1000-char chunks with 200-char overlap.
- *What it produced:* A `split_text()` that splits on sentence boundaries (`. `), packs sentences up to MAX_CHARS, and seeds the next chunk with the trailing OVERLAP_CHARS of the previous one. `chunk_data()` looped over professors, skipped empty comments, called `split_text()`, and returned a flat list of chunk dicts with nested Professor/Review structure.
- *What I changed or overrode:* The AI's initial `chunk_data()` used a global chunk counter for IDs. I overrode it to use `f"{name}-{review_index}-{piece_index}"` so IDs encode which professor and review they came from, making debugging and tracing much easier.

**Instance 2**

- *What I gave the AI:* The runtime traceback showing a `KeyError: 'Professor'` when `format_context()` was called, along with both `retriever.py` and `generator.py`.
- *What it produced:* An explanation that `retrieve()` returns flat chunks (keys: `id`, `text`, `metadata`) while `format_context()` was written to consume nested chunks (keys: `Professor`, `Review`). It produced a corrected `format_context()` that reads `chunk["metadata"]["professor"]`, `chunk["text"]`, and the flat metadata keys instead of the nested ones.
- *What I changed or overrode:* The AI also fixed the `lines` list bug in the same pass — the original code reassigned `lines` as a string after the loop rather than appending to it, so only the last chunk was ever included in the context. I kept both fixes since both were genuine bugs.
