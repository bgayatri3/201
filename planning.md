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
| 1 | Vanguard | Early retirement and the 4% rule: How FIRE investors can succeed | https://investor.vanguard.com/investor-resources-education/retirement/early-retirement |
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

**Chunk size:** paragraph sized chunks (fixed size chunks)

**Overlap:** 10-20% overlap

**Reasoning:** More inquiries can be sufficently answered in a paragraph. For the articles selected in the links above, paragraphs and headings/subheadings are already used. This will make it easier to create definitive chunks. For more forum based documents (like Reddit), responses to the thread often do not span over a paragraph or are already separated into paragraphs. To be more specific, somewhere between 300-800 characters should be ideal. 

Additionally, the 10-20% overlap will help preserve concepts across more complex financial concepts that span over multiple paragraphs. This could include ideas like is the 4% rule accurate, which might have more detailed nuanced. The overlap will help reduce the risk of retrieving incomplete information for cases like this

**Implementation note (Milestone 3):** Implemented in `src/chunk.py` with LangChain's `RecursiveCharacterTextSplitter`, `chunk_size=800`, `chunk_overlap=120` (15%, mid-range of the planned 10-20%), splitting on paragraph → line → sentence → word boundaries so chunks are never cut mid-word. Added a `MIN_CHUNK=200` post-step that merges sub-200-char fragments (e.g. a lone `## heading` line, or a short trailing scrap) into a neighboring chunk — this wasn't in the original spec, but inspection showed the splitter occasionally emits standalone heading fragments with no retrievable meaning, so merging keeps every chunk a complete thought. Cleaning (in `src/ingest.py`) also strips link-only list items (related-article / "in this article" navigation widgets on Investopedia and JL Collins) that would otherwise produce link-list chunks. **Final count: 151 chunks across all 10 sources (min 299 / mean 655 / max 799 chars).** 6 sources are scraped live; the 4 anti-bot-blocked sources (both Reddit threads, Bogleheads, US News) are ingested from browser-saved files in `documents/manual/`, which override scraping and run through the same cleaning + chunking pipeline.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** This embedding model was chosen because it is lightweight and still effectively captures the semantic meaning of the text. Some aspects such as intro to FIRE is a little repetitive across some documents (especially intro paragraphs). So, this model does a good job of converting the text to a 384-dimension vector to cluster and group similar sentences. However, it has a relatively short context window and struggles with very lengthy passaes. 

If deployed for real users and cost wasn't a constraint, another model (like on of OpenAI's or Anthropic's) would be even more ideal. The retrieval accuracy is better, and it might do a better job of interpreting complicated financial concepts. I would optimize for things such throughput, especially as more users put more strain on the system and its ability to process requests. Latency, time from user query submission to reponse, is also very important for overall user experience. Secondary priorities include multilingual options and supporting both semantic questions and numerical calculations plus visualizations of personalized retirement data. 

Source: https://medium.com/@rahultiwari065/unlocking-the-power-of-sentence-embeddings-with-all-minilm-l6-v2-7d6589a5f0aa 
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the difference between Lean Fire and Fat Fire? | Lean FIRE involves retiring on a relatively low annual budget, while Fat FIRE involves accumulating enough wealth to support a higher-spending lifestyle. |
| 2 | Why is diversification important when considering FIRE strategies?| Diversification spreads investments across multiple assets to reduce risk and portfolio volatility. |
| 3 | What are two commonly cited advantages and disadvantages of pursuing FIRE? | Advantages include financial freedom and flexibility. Disadvantages include high savings requirements and potential lifestyle sacrifices. |
| 4 | How is an FI number calculated?| A common estimate is annual expenses multiplied by 25, based on the 4% rule. |
| 5 | What are common investment recommendations in the FIRE community?| Low-cost index funds, diversified stock funds, and tax-advantaged retirement accounts are frequently recommended. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Inconsistency in documents may make it hard for the model to retrieve a single answer (with the given chunk size/context). There is not just one method for achieving FIRE, and people have various opinions on how to best achieve it. There is a lot of nuance in some answers since there is not just a one size fits all solution. 

2. The chunking size is appropriate for most questions. However, some questions can not be adequately answered by a single paragraph. Some sections in the documents include longer passages which may result in the system returning incomplete explanations. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

┌───────────────────────────────────────────────────┐                                                                             
│                                                   │                                                                             
│                  Document Ingestion               │                                                                             
│                                                   │                                                                             
│     Python script to turn links into .txt files   │                                                                             
│       for chunking (Beautiful Soup library)       │                                                                             
└──────────────────────────┬────────────────────────┘                                                                             
                           │                                                                                                      
                           │                                                                                                      
┌──────────────────────────▼────────────────────────┐                                                                             
│                                                   │                                                                             
│                     Chunking                      │                                                                             
│                                                   │                                                                             
│          LangChain Text Splitters (library)       │                                                                             
│                to create chunk_text()             │                                                                             
└─────────────────────────┬─────────────────────────┘                                                                             
                          │                                                                                                       
                          │                                                                                                       
┌─────────────────────────▼─────────────────────────┐                                                                             
│                                                   │                                                                             
│              Embedding + Vector Store             │                                                                             
│                                                   │                                                                             
│            all-MiniLM-L6-v2 and ChromaDB          │                                                                             
│                                                   │                                                                             
└──────────────────────────┬────────────────────────┘                                                                             
                           │                                                                                                      
                           │                                                                                                      
┌──────────────────────────▼────────────────────────┐                                                                             
│                                                   │                                                                             
│                       Retrieval                   │                                                                             
│                                                   │                                                                             
│         ChromaDB similarity search (top k=5)      │                                                                             
│                                                   │                                                                             
└──────────────────────────┬────────────────────────┘                                                                             
                           │                                                                                                      
                           │                                                                                                      
┌──────────────────────────▼────────────────────────┐                                                                             
│                                                   │                                                                             
│                     Generation                    │                                                                             
│                                                   │                                                                             
│                   Groq as the LLM                 │                                                                             
│                                                   │                                                                             
└───────────────────────────────────────────────────┘                                                                             

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

1. Document Ingestion
- AI Tool: Claude
- Input: 10 hyperlinks of reddit pages, and posts (Documents subheading)
- Output: title_of_link.txt file (so 10 txt files, one for each link) containing the content of the links via scraping 
- Verification: Confirm all documents are loaded and cleaned (no html tags, or unexpected spaces)

2. Chunking
- AI Tool: Claude to make chunk_text()
- Input: 10 txt files are used to make paragraph sized chunks (reference Chunking Strategy subheading)
- Output: Code for chunk_text() function which generated 50-2000 overlapping chunks, each chunk should also include its corresponding source filename 
- Verification: Inspect sample chunks, ensure no empty chunks, chunks should not be split mechanically and instead content boundies must be respected

3. Embeddings and Vector Store
- AI Tool: Claude 
- Input: Chunks are processed using all-MiniLM-L6-v2 and ChromaDB (reference Retrieval Approach subheading )
- Output: Code that generates the embeddings and stores them into a vector database
- Verification: Confirm vectors are created and stored without errors, each chunk gets its own unique emebedding

4. Retrieval
- AI Tool: Claude
- Input: Requirements to retrieve the top 5 most relevant chinks
- Output: A retrieval function that accepts a query string and returns the top-k most relevant chunks along with their source information, include the distance as well 
- Verification: test with 3 known questions (reference Evaluation Plan subheading) and confirm that the relevant chunks are returned, ensure that results are comming from the correct source, distance scores should be below 0.7 (ideally below 0.5), chunks retrieved should not look like fragments or HTML leftovers

5. Generation
- AI Tool: Claude code
- Input: retrieved chunks, user query
- Output: Prompt template and generation code for answering questions using retrieved context. 
- Verification: Compare responses against the expected answers listed in the Evaluation Plan and check that answers are grounded in retrieved documents.


**Milestone 3 — Ingestion and chunking:**
Below are the results of my small script chunk_check.py. The 5 chunks below are decent. This exercise helped me remove some misc data still present in the txt files.

================================================================================
ID: saxo_fire_guide.txt::chunk_0
Source: saxo_fire_guide.txt
Length: 496 chars
--------------------------------------------------------------------------------
## Financial Independence Retire Early (FIRE): Guide

Saxo Group

## A new path to financial independence

For decades, retirement felt like a fixed destination: you worked until 65 or 67, collected a pension, maybe a gold watch, and that was the end of the story. But in recent years, a movement has emerged that challenges these traditions and reimagines what retirement and investing strategies can look like.

That movement is FIRE: Financial Independence, Retire Early.

## FIRE fundamentals


================================================================================
ID: sofi_pros_cons_fire.txt::chunk_15
Source: sofi_pros_cons_fire.txt
Length: 608 chars
--------------------------------------------------------------------------------
## Dividends

Shareholders earn dividend income when companies have excess profits. Dividends are generally offered on a quarterly basis, and if you hold shares of a stock you could earn them.

However, because dividend payments depend on company performance, they’re not guaranteed. Those relying on them to live should have other income sources (including substantial savings accounts) as a back up income stream.

## Market Appreciation

Investors can also earn potential profits through market appreciation when they sell stocks and other assets for a higher price than what they initially paid for them.


================================================================================
ID: jlcollins_401k_403b_tsp_ira_roth_buckets.txt::chunk_19
Source: jlcollins_401k_403b_tsp_ira_roth_buckets.txt
Length: 730 chars
--------------------------------------------------------------------------------
There is no RMD.

In short, these can be summarized like this:

401(k)/401(b)/TSP = Immediate tax benefits and tax-free growth. No income limit means the tax deduction for high income earners can be especially attractive. But taxes are due when the money is withdrawn.

Roth 401(k) = No immediate tax benefit, tax-free growth and no taxes due on withdrawal.

Deductible IRA = Immediate tax benefits and tax-free growth. But taxes are due when the money is withdrawn. Deductibility is phased out over certain income levels.

Non-Deductible IRA = No immediate tax benefit, tax-free growth and added complexity. Taxes are due only on the account’s earnings when the money is withdrawn. Contributions can be made regardless of income.


================================================================================
ID: jlcollins_401k_403b_tsp_ira_roth_buckets.txt::chunk_4
Source: jlcollins_401k_403b_tsp_ira_roth_buckets.txt
Length: 508 chars
--------------------------------------------------------------------------------
Investments that are “tax-inefficient” are those that pay interest, non-qualified dividends and those that generate taxable capital gains distributions. These are things like some stock funds, bonds, CDs and REITs (real estate investment trusts). These we want to keep ideally in our tax-advantaged buckets as their payouts are then tax-deferred.

There are several variations of tax-advantaged buckets, and we’ll look at each. But first let’s look at our three investments and consider where they might fit:


================================================================================
ID: sofi_pros_cons_fire.txt::chunk_1
Source: sofi_pros_cons_fire.txt
Length: 694 chars
--------------------------------------------------------------------------------
While it may sound like the perfect life hack, attempting to live out this dream comes with some serious challenges. Read on to learn more about the FIRE movement and some techniques followers have used to help achieve their goal of early retirement. That can help you determine whether any of their savings strategies might be right for you.

Key Points

• FIRE stands for Financial Independence, Retire Early, with proponents aiming to retire earlier than the traditional time frame of 65 to 70 years-old.

• The movement originated from the book Your Money or Your Life in 1992, and gained traction in the 2010s.

• Achieving FIRE may require saving 50% to 75% of income and living frugally.

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
