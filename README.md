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
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
