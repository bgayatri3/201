# The Unofficial Guide — Project 1


---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

FIRE (Financial Independence, Retire Early) for Early-Career Professionals - useful because there is a lot of useful information in niche places, misconceptions or lack of transparency around finances, and overall financial unawareness surrounding how young people can set themselves up for finanical freedom. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** paragraph sized chunks (fixed size chunks of 300-800 characters)

**Overlap:** 10-20% overlap

**Why these choices fit your documents:** More inquiries can be sufficently answered in a paragraph. For the articles selected in the links above, paragraphs and headings/subheadings are already used. This will make it easier to create definitive chunks. For more forum based documents (like Reddit), responses to the thread often do not span over a paragraph or are already separated into paragraphs. 

Additionally, the 10-20% overlap will help preserve concepts across more complex financial concepts that span over multiple paragraphs. This could include ideas like is the 4% rule accurate, which might have more detailed nuance. The overlap will help reduce the risk of retrieving incomplete information for cases like this.

Some preprocessing was done such as stripping any HTML tags, advertisements, or unrelated linked topics. Beautiful soup was utilized to extract the main information body for 6/10 of the links. Then, certain junk widgets were also removed. For example, text such as "you might also like" or "skip to main content" or "table of contents" were all deleted. Claude had diffculty extracting information from Reddit, USNews, and a Vanguard wiki. This was because some scraping restrictions were inplace, so I had it format the main body manually. Lastly, the text document preserved headings using markdown to make it easier for the chunking stage. 

**Final chunk count:** 151 (chars=299 - 799, average = 655)

**Sample chunks: **
| # | ID | Length | Chunk |
|---|--------|--------|-----------------|
| 1 | jlcollins_401k_403b_tsp_ira_roth_buckets.txt::chunk_9 | 747 chars  | From Go Curry Cracker: From The Mad Fientist: Here on jlcollinsnh: There are many, many variations of 401(k)-type and IRA-type accounts. We’ll look at the basic types here. The rest are branches from these trees. Employer-based tax-advantaged buckets These are buckets provided by your employer. They select an investment company which then offers a selection of investments from which to choose. Many employers will match your contribution up to a certain amount. The amount you can contribute is capped. For 2015 the cap is $18,000 per year and $24,000 for those age 50 and older. You can contribute to more than one plan (if you have access to more than one) but the cap is the total for all together, not for each separately. In general: |
| 2 | reddit_best_toughest_lessons.txt::chunk_10 | 678 chars  | ## Spending Matters as Much as Income A central FIRE principle is: Income alone does not create wealth. Examples: - Earning $1 million and spending $1 million produces little progress. - Spending less than you earn creates the ability to invest and build wealth. Both income and expenses matter ## Balance Financial Goals With Enjoying Life Financial efficiency should not come at the expense of meaningful experiences. Many contributors emphasized:- Spend time with family.- Enjoy experiences while you are healthy.- Do not sacrifice everything for a larger future portfolio. A sustainable FIRE plan balances future goals with present enjoyment.## Key Takeaways |
| 3 | investopedia_fire_explained.txt::chunk_10 | 774 chars  | ## What Are the Pros and Cons of the FIRE Movement? You can adjust the details of your FIRE plan to fit your particular situation. There are also several variations, from Fat FIRE to Lean FIRE. However, saving aggressively may not be realistic for some, especially for those who care for children or elderly parents. And inflation or a bear market before you want to retire could make that goal difficult, forcing you to adjust your plans. ## How Does FIRE Differ From Micro-Retirement? Unlike full early retirement, micro-retirement involves planned career breaks that offer flexibility without complete financial independence. For example, someone might take a year-long break in their 40s or 50s to travel the world and then reenter the job market.|
| 4 | jlcollins_early_retirement_withdrawal_roth_ladder.txt | 364 chars  |  To build up his $12,800 conversion ladder, he moves $12,800 from his Traditional IRA to his Roth IRA every year. After the fifth year, he is then able to withdraw $12,800 per year from the account. Assuming he continues to convert $12,800 every year, he will be able to withdraw $12,800 from his Roth IRA, tax and penalty free, every year for the rest of his life. |
| 5 | saxo_fire_guide.txt::chunk_22 | 703 chars  | But keep in mind that economic conditions are also changing constantly, so it’s important to revisit your retirement calculations regularly. The last thing you want as a FIRE follower is to plan for a financial future that’s no longer available.## Plan, don’t play, with FIRE Financial independence doesn’t just happen – it takes careful planning. But where do you start? Try these four short-term actions first: Analyse your annual expenses to see how much you’ll need to save (25 times). Set up an automated monthly investment plan to maximise saving efficiency. Choose your investment vehicles that reduce tax impact. Plan multiple income streams from dividend stocks, real estate investments.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** This embedding model was chosen because it is lightweight and still effectively captures the semantic meaning of the text. Some aspects such as intro to FIRE is a little repetitive across some documents (especially intro paragraphs). So, this model does a good job of converting the text to a 384-dimension vector to cluster and group similar sentences. However, it has a relatively short context window and struggles with very lengthy passaes. 

If deployed for real users and cost wasn't a constraint, another model (like on of OpenAI's or Anthropic's) would be even more ideal. The retrieval accuracy is better, and it might do a better job of interpreting complicated financial concepts. I would optimize for things such throughput, especially as more users put more strain on the system and its ability to process requests. Latency, time from user query submission to reponse, is also very important for overall user experience. Secondary priorities include multilingual options and supporting both semantic questions and numerical calculations including visualizations of personalized retirement data. 

**Sample Retrieval: **
| # | Query | Top 5 Chunks | Best Distance |
|---|-------|--------------|---------------|
| 1 | What is the difference between Lean FIRE and Fat FIRE? | **1. investopedia_fire_explained.txt (chunk 4)** — "FIRE Variations Explained: Lean FIRE, Fat FIRE, Barista FIRE & More... Fat FIRE: for people who want to save substantially more than the average worker but don’t want to reduce their current standard of living..."<br><br>**2. saxo_fire_guide.txt (chunk 6)** — "Lean FIRE: This frugal form of FIRE is focused on minimalism..."<br><br>**3. usnews_7_lessons_fire.txt (chunk 2)** — "Lean FIRE, Fat FIRE, Barista FIRE, Coast FIRE..."<br><br>**4. saxo_fire_guide.txt (chunk 5)** — "Plenty of financial cushion; freedom to maintain or even upgrade your lifestyle..."<br><br>**5. saxo_fire_guide.txt (chunk 4)** — "FIRE flavours... traditional FIRE model focuses on accumulating wealth..." | 0.352 (strong) |
| 2 | Why is diversification important when considering FIRE strategies? | **1. saxo_fire_guide.txt (chunk 2)** — "FIRE practitioners typically save 50–70% of their income..."<br><br>**2. saxo_fire_guide.txt (chunk 4)** — "The traditional FIRE model focuses on accumulating wealth..."<br><br>**3. saxo_fire_guide.txt (chunk 23)** — "Plan multiple income streams from dividend stocks, real estate investments..."<br><br>**4. saxo_fire_guide.txt (chunk 26)** — "FIRE is for anyone who wants their own path to financial independence..."<br><br>**5. saxo_fire_guide.txt (chunk 12)** — "Diversification means spreading your investment money across a wider range of sectors, industries, regions and asset types..." | 0.364 (strong) |
| 3 | How is an FI number calculated? | **1. reddit_financialindependence_faq.txt (chunk 1)** — "FI relies on investing savings so money can grow over time..."<br><br>**2. reddit_financialindependence_faq.txt (chunk 0)** — "Financial Independence (FI) is having enough income from investments..."<br><br>**3. reddit_financialindependence_faq.txt (chunk 2)** — "Required Portfolio = Annual Expenses × 25..."<br><br>**4. reddit_financialindependence_faq.txt (chunk 4)** — "Many FI investors prefer passive investing..."<br><br>**5. jlcollins_early_retirement_withdrawal_roth_ladder.txt (chunk 18)** — "The Mad Fientist expanded these concepts..." | 0.603 (weak) |
| 4 | What are common investment recommendations in the FIRE community? | **1. saxo_fire_guide.txt (chunk 2)** — "FIRE practitioners typically save 50–70% of their income..."<br><br>**2. saxo_fire_guide.txt (chunk 10)** — "Getting there depends on aggressive saving and disciplined investing..."<br><br>**3. reddit_best_toughest_lessons.txt (chunk 8)** — "Build the life you want, then save for it..."<br><br>**4. saxo_fire_guide.txt (chunk 23)** — "Plan multiple income streams from dividend stocks, real estate investments..."<br><br>**5. saxo_fire_guide.txt (chunk 25)** — "Critics point out that very few people are actually reaching the goal of early retirement..." | 0.344 (strong) |

**Explanation for 1:** 

**Explanation for 2:** 
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** In ```query.py``` the following system prompt is used
```
SYSTEM_PROMPT = (
    "You are a factual assistant for questions about FIRE (Financial "
    "Independence, Retire Early). Answer the user's question using ONLY the "
    "information in the numbered context documents provided in the user "
    "message. Follow these rules strictly:\n"
    "1. Do NOT use any outside or prior knowledge. Every claim in your answer "
    "must be supported by the context.\n"
    "2. If the context does not contain enough information to answer, reply "
    f"with exactly: \"{REFUSAL}\" and nothing else.\n"
    "3. Do not invent facts, numbers, or sources.\n"
    "4. Be concise and directly answer the question."
)
```
It was emphasized to the LLM that answers must be grounded in the 10 documents given. This was especially important because without it the model could potentially use its own pre-existing training data, rather than the information given. I also gave Claude the good/bad example from the Milestone 5 sections as a template to work off of. 


**How source attribution is surfaced in the response:**  Source attribution is assembled PROGRAMMATICALLY from the retrieved chunks' metadata (result["sources"]) — the LLM never invents which document an answer came from. 

Here is an example, below each response

<img width="601" height="89" alt="image" src="https://github.com/user-attachments/assets/f018686d-cc34-4ca2-a576-ce6a10bcb13d" />


---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the difference between Lean Fire and Fat Fire? | Lean FIRE involves retiring on a relatively low annual budget, while Fat FIRE involves accumulating enough wealth to support a higher-spending lifestyle| Lean FIRE involves a minimalist and extreme saver lifestyle... Fat FIRE, on the other hand, is for people who want to save substantially more than the average worker without reducing their current standard of living.| Relevant | Accurate |
| 2 | Why is diversification important when considering FIRE strategies? | Diversification spreads investments across multiple assets to reduce risk and portfolio volatility. | Diversification is important because it means spreading your investment money across a wider range ... This helps protect your portfolio from market volatility, as if one investment weakens, your other investments can help cushion the blow. | Partially relevant | Accurate |
| 3 | What are two commonly cited advantages and disadvantages of pursuing FIRE? | Advantages include financial freedom and flexibility. Disadvantages include high savings requirements and potential lifestyle sacrifices.| Two commonly cited advantages of pursuing FIRE are: 1. Having more flexibility with your time and ... Two commonly cited disadvantages of pursuing FIRE are: 1. The unpredictability of the future and... | Relevant | Accurate |
| 4 | How is an FI number calculated? | A common estimate is annual expenses multiplied by 25, based on the 4% rule. | The FI number, also referred to as the "Required Portfolio", can be calculated using the formula: Required Portfolio = Annual Expenses × 25. | Relevant | Accurate |
| 5 | What are common investment recommendations in the FIRE community? | Low-cost index funds, diversified stock funds, and tax-advantaged retirement accounts are frequently recommended.| Common investment recommendations in the FIRE community include: - Broadly diversified ETFs and index funds, minimising management fees. - Broad-market index funds.| Partially relevant | Accurate|

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

**Question that failed:** How much should I save every month to reach FIRE?

**What the system returned:** The amount you should save each month is up to you, but examples given are USD 100 or 300. The more you save, the more you can invest, and the sooner you may be able to reach financial independence.

**Root cause (tied to a specific pipeline stage):** It is likely the retrieval stage here, and possibly the generation could be another issue. It is likely that chunk has a weaker/higher distance score. When I looked through what specific chunk was retrieved, that chunk was an example of how compounding interest works (ex $100 a month over x period of time compounds) rather than a chunk relating to a specific saving recommendation like in the query. Since the retrieval system returned a loosely related chunk, the model generated an overly specific answer that is missing the complete context. 

**What you would change to fix it:** The easiest fix would be to modify the generation prompt. The model should be able to distinguish between examples and direct recommendations. The 10 documents provide general tips and advice, and since each individual's finances are nuanced, it isn't best equipped to provide that kind of individualized advice. When posed these kinds of personal questions, the model should state its limitation and provide general advice instead. Some experimentation with retrieving k chunks or adding more equations/math in the documents/chunks could also be explored. 

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The spec helped breakdown the larger task into actionable and testable smaller sections. The debugging sections for each milestone helped me give do's and don't to the model when generating code. I also was more equipped to handle the challenges such as potentially scrapping issues since I was made aware of it when writing the planning.md. Through this document, I had both the higher level overview of how the system connected (i.e the architecture diagram), as well as minor details such as specific libraries and recommendations for each step. 

**One way your implementation diverged from the spec, and why:** After each stage, I did a combination of manual and separate scripting to test each milestone independently. For example, I read through the .txt files to ensure that any miscellaneous tags were not kept. This allowed me to make minor code tweaks to remove that information from the Claude generated scripts. I also deleted large useless sections. Another instance, was printing out 5 random chunks in my check_chunks.py and manually inspecting them. I followed a similar process for the retrieval and generations stages as well. I caught some early mistakes manually (particularly with the F1 number question) and was able to correct mistakes in my .txt file. 

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

- *What I gave the AI:* I gave Claude my Retrieval section from planning.md and asked it to implement a way to test/print the top 5 hits. 
- *What it produced:* Originally, it listed a very small snippet of the chunk. This made it harder to me to determine whether the chunk as a whole was useful. 
- *What I changed or overrode:* For testing purposes, I lengthed the size of the snippet to make it easier to evalute its relevance to the query. 

**Instance 2**

- *What I gave the AI:* A direct link to reddit url for scraping 
- *What it produced:* An empty .txt because of anti-bot restrictions on scraping 
- *What I changed or overrode:* I changed the input to be the top comments of the .json version of the reddit pages. It was then able to take the top reddit comments and format them into the md format to make it easier for the chunking stage. 
