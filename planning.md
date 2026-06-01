# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
FIRE (Financial Independence, Retire Early) for Early-Career Professionals is valuable because there is a lot of useful information in niche places and misconceptions or lack of transparency around finances in general. Many financial institutions offer surface level advice online to give basic education on FIRE topics. More helpful tips and strategies can be uncovered through spiralling through long and dated reddit threads. By aggregating and simplifying this data, young people can utilize these tools and techniques early to boost their chances to hit this goal. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Vanguard | Early retirement and the 4% rule: How FIRE investors can succeed | https://investor.vanguard.com investor-resources-education/retirement/early-retirement |
| 2 | Investopedia | FIRE Explained: Financial Independence, Retire Early – Rules, Types & Planning | https://www.investopedia.com/terms/f/financial-independence-retire-early-fire.asp |
| 3 | r/financialindependence | The Basics |https://www.reddit.com/r/financialindependence/wiki/faq/ |
| 4 | Saxo | Financial Independence Retire Early (FIRE): Guide | https://www.home.saxo/learn/guides/trading-strategies/financial-independence-retire-early-fire-a-guide |
| 5 | r/financialindependence | Best and toughest lessons your learned on your FIRE journey | https://www.reddit.com/r/financialindependence/comments/1nawcca/best_and_toughest_lessons_your_learned_on_your/ |
| 6 | Bogleheads | Three-fund portfolio | https://www.bogleheads.org/wiki/Three-fund_portfolio |
| 7 | JL Collins | The 401(k), 403(b), TSP, IRA & Roth Buckets | https://jlcollinsnh.com/2015/06/02/stocks-part-viii-the-401k-403b-tsp-ira-roth-buckets/ |
| 8 | JL Collins | Early Retirement Withdrawal Strategies and Roth Conversion Ladders from a Mad Fientist | https://jlcollinsnh.com/2013/12/05/stocks-part-xx-early-retirement-withdrawal-strategies-and-roth-conversion-ladders-from-a-mad-fientist/ |
| 9 | US News | 7 Lessons From Those Who Retired by FIRE | https://money.usnews.com/money/retirement/aging/articles/lessons-from-those-who-retired-by-fire |
| 10 | Sofi | Pros & Cons of FIRE | https://www.sofi.com/learn/content/pros-cons-of-fire-movement/|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

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

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
