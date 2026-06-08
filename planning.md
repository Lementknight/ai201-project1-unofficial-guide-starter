# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

How to navigate your employee benefits as a new grad hire. This knowledge is valuable because a company's benefits package is very important to understand. Most new hire are new to the entire process so a guide would be a great resource for people.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Anders CPA — Understanding Employee Benefits: A Guide for Recent Graduates | New-grad orientation: waiting periods, how elections work | https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/ |
| 2 | TurboTax — Guide to Your Employer's Benefits Programs, Tax-Wise (401(k), HSA, FSA) | Tax mechanics of 401(k) match, HSA triple-tax-advantage, FSA use-it-or-lose-it | https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz |
| 3 | First Hawaiian Bank — Workplace Financial Benefits: A Beginner's Guide | Beginner framing of retirement/financial benefits from a bank's POV | https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide |
| 4 | MetLife — HDHP vs. Traditional PPO 2026 | Choosing a health plan; 2026 deductible/contribution numbers | https://www.metlife.com/stories/benefits/hdhp-vs-ppo/ |
| 5 | Cigna — HDHP vs. PPO Plans: What's the Difference? | Second payer perspective on plan networks & cost trade-offs | https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans |
| 6 | U.S. Dept. of Labor — ERISA / Health Plans | Authoritative source on legal rights & the Summary Plan Description | https://www.dol.gov/general/topic/health-plans/erisa |
| 7 | U.S. DOL EBSA — Filing a Claim for Your Health Benefits | What to do when a claim is denied; appeals timelines | https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/publications/filing-a-claim-for-your-health-benefits |
| 8 | Woven Capital — How to Evaluate Equity Compensation in Your First Tech Job Offer (RSUs, Options, Vesting) | Equity comp, vesting cliffs, RSU tax surprises for first-job hires | https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/ |
| 9 | Reddit r/personalfinance — "Prime Directive" wiki / common topics | Community order-of-operations (match → debt → emergency fund → HSA → Roth) | https://www.reddit.com/r/personalfinance/wiki/commontopics |
| 10 | Randstad — How to Negotiate Benefits to Maximize Your Job Offer | Negotiating PTO, signing bonus, tuition reimbursement beyond salary | https://www.randstadusa.com/job-seeker/career-advice/salary/how-to-negotiate-benefits-package/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 1,000–1,500 characters (approximately 300–512 tokens, or 200–300 words)

**Overlap:** 100–200 characters (10–15% of chunk size)

**Reasoning:** The sources are educational guides and explainers with clear semantic sections (401(k), HSA vs. FSA, HDHP vs. PPO, vesting schedules, tax implications, negotiation tactics). Each section is a complete concept that deserves space to explain fully. A 1000–1500 char chunk captures one coherent topic without fragmenting explanations—e.g., "how HSA triple-tax-advantage works" stays intact instead of being split across chunks. Overlap helps capture concept bridges: "401(k) match" appears in both the "401(k) section" and the "funding priorities" section, so a small overlap ensures retrieval of both mentions. This avoids two extremes: chunks that are too large (2000+ chars combining 401(k) + HSA + FSA into one noisy chunk) and too small (<500 chars that split definitions across boundaries and lose explanatory context).

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-mpnet-base-v2` via sentence-transformers (768 dimensions)

**Top-k:** 3

**Production tradeoff reflection:** For production, if cost and latency were not constraints, I would use a fine-tuned embedding model trained on HR/benefits Q&A pairs (e.g., a domain-specific variant of E5-large or BGE-large-en-v1.5). This would better capture subtle distinctions in benefits language (e.g., "vesting cliff" vs. "waiting period" vs. "cliff year") and improve recall on employee-specific terminology. Alternatively, I could pair `all-mpnet-base-v2` with a reranker (e.g., cross-encoder) to re-rank the top-k results by relevance, boosting accuracy without fully retraining. The tradeoff is latency and infrastructure complexity—for a student project, `all-mpnet-base-v2` + top-k=3 is the right balance of accuracy, speed, and simplicity.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Why should someone choose to max out their medical FSA account? | You should max out your medical FSA only if you have predictable medical expenses (prescriptions, glasses, copays) that you'll incur within the plan year, because contributions are pre-tax. However, medical FSAs have a strict "use it or lose it" rule—unused money is forfeited (though some employers allow a small grace period or up to $610 carryover in 2026)—so you shouldn't max out if you're uncertain about expenses. |
| 2 | If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth? | Yes, you must remain with the company until the shares vest (mature). If you leave before 5 years, unvested shares are forfeited and you lose that equity compensation. However, once shares vest and are delivered to you, you own them and they can't be clawed back if you leave. |
| 3 | If I am already covered for health insurance, should I even consider enrolling in my company's plan? | Yes, you should consider enrolling in your company's plan because employer plans typically offer better coverage and lower costs than individual plans, plus employers often contribute to premiums, deductibles, or HSA/FSA accounts. You may also face coordination-of-benefits questions and tax implications. |
| 4 | What is open enrollment? | Open enrollment is the annual period (typically once per year, often in the fall) when employees can enroll in, change, or drop their benefits plans. Outside of open enrollment, you can only change elections if you experience a qualifying life event (marriage, birth, job loss, etc.). |
| 5 | What is the difference between PTO, short-term disability, and long-term disability? | PTO (paid time off) covers vacation, sick days, and personal days that you can use at your discretion. Short-term disability replaces a portion of your salary when a medical issue prevents you from working, typically lasting weeks to months. Long-term disability replaces a portion of salary for longer absences, starting when short-term disability ends and potentially lasting until retirement. |
| 6 | What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket? | Commuter benefits allow you to pay for public transit, parking, or vanpool costs with pre-tax dollars, reducing your taxable income and saving on taxes. Unlike medical FSAs, commuter benefit plans often allow unused funds to roll over to the next year (check your plan), making them a lower-risk savings option for predictable commuting costs. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Outdated regulatory and contribution limit information.** My sources cite 2026 limits (HSA $4,400, 401(k) $24,500), but these change annually. If a new hire in 2027 asks "what's the HSA contribution limit," my system will retrieve 2026 data and confidently return an outdated answer. Without a mechanism to update or flag stale information, the system becomes unreliable over time.

2. **Chunking splits decision-critical distinctions.** For example, the rules for medical FSA (strict use-it-or-lose-it) versus commuter FSA (rollover allowed) might be separated across chunk boundaries or different sources. A query like "can I roll over FSA funds?" could retrieve only the medical FSA chunk and miss the commuter benefit exception, returning an incomplete or incorrect answer. The semantic meaning required to answer the question is split across multiple chunks.

3. **Off-topic retrieval noise.** My sources discuss benefits, but also weave in tax optimization, career negotiation, financial planning, and ERISA legal rights. A query like "how should I invest my 401(k)" might retrieve investment advice tangentially related to 401(k)s but not what a new hire asking "how much should I contribute" actually needs. The system confuses benefits administration with personal finance strategy.

4. **Conflicting advice without source attribution.** Cigna and MetLife might give slightly different recommendations on HDHP vs. PPO (e.g., "good for young healthy people" vs. "depends on your medical history"). My system could retrieve both perspectives without surfacing which source said what, whether they contradict, or whether one is more credible—leaving the new hire confused.

5. **Questions requiring company-specific data and hidden policies.** A new hire's actual question is "what's *my* company's 401(k) match?" or "how many vacation days *do I* get?" My corpus provides general guidance ("most companies offer X") but can't answer the person's specific package. This is further complicated by policies that lack clear answers: some companies offer "unlimited PTO" or "flexible PTO approved ad-hoc," which have no fixed limit but are governed by company culture and manager discretion—my system can explain what these mean in theory but can't capture the lived reality of how they work at a specific company. The system might confidently return generic answers, and the new hire walks away with unrealistic expectations about their actual compensation.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            RAG Pipeline Architecture                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Document Ingestion    Chunking         Embedding + Store    Retrieval  Gen. │
│  ───────────────────   ────────────     ─────────────────    ────────── ──  │
│                                                                               │
│  • 10 sources         Semantic          • all-mpnet-base-v2  ChromaDB   Groq│
│  • Web URLs & blogs   chunking:         • 768 dimensions     semantic   API │
│  • Python requests/   • 1000-1500       • ChromaDB vector    search     call│
│    BeautifulSoup      chars per chunk   store (in-memory)   • top-k=3      │
│  • Extract plain text • 10-15% overlap  • Persist to disk                   │
│                       • Preserve                                             │
│                         section                                              │
│                         boundaries                                           │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

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

- **AI tool:** Claude
- **Input:** Planning.md sections (Documents table with 10 URLs, Chunking Strategy with 1000–1500 char / 100–200 char overlap targets, Anticipated Challenges #2 about chunk splitting). I'll also provide one sample benefits guide URL for reference.
- **Expected output:** Python script with `fetch_and_parse(url)` function (using requests + BeautifulSoup to extract text) and `chunk_text(text, chunk_size=1500, overlap=200)` function that respects semantic boundaries (section headers).
- **Verification:** Run the script on one live source, spot-check that chunks are 1000–1500 chars, overlap is present, and a complete concept (e.g., "HSA definition + tax advantages") stays in one chunk, not split.

**Milestone 4 — Embedding and retrieval:**

- **AI tool:** Claude
- **Input:** Planning.md sections (Retrieval Approach specifying all-mpnet-base-v2 and top-k=3, Architecture diagram, Anticipated Challenges #3 about off-topic noise). I'll provide sample chunks from Milestone 3 output and one test question.
- **Expected output:** Python script using sentence-transformers (`all-mpnet-base-v2`) to embed chunks and ChromaDB to store/persist them. Include a `retrieve(query, top_k=3)` function that returns the 3 most semantically similar chunks and their source URLs.
- **Verification:** Query the system with 2–3 test questions, confirm that retrieved chunks are topically relevant and that off-topic content is ranked lower than relevant content.

**Milestone 5 — Generation and interface:**

- **AI tool:** Claude
- **Input:** Planning.md sections (Evaluation Plan with 6 test questions + expected answers, Anticipated Challenges #4 and #5 about conflicting advice and company-specific data). I'll provide the full retrieval system from Milestone 4 and system prompt requirements for grounding.
- **Expected output:** Python script that (1) formats retrieved chunks into a grounded context prompt, (2) calls Groq API with a system prompt that enforces staying within retrieved documents, (3) returns the LLM response plus source attribution (URLs of chunks used). Include a simple interface (CLI or Gradio) to test queries.
- **Verification:** Run all 6 evaluation questions through the full pipeline, check that responses are accurate based on expected answers, identify which anticipated challenges manifest (e.g., conflicting advice, company-specific limits), and document in a test report.
