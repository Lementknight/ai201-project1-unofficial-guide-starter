# RAG Pipeline Implementation — Quick Start

## Files Created

- **ingest.py** — Milestone 3: Scrapes 10 sources, chunks semantically, saves JSON
- **embed.py** — Milestone 4: Embeds chunks with all-mpnet-base-v2, stores in ChromaDB
- **query.py** — Milestone 5: Gradio web UI + Groq LLM for grounded answers

## Setup

### 1. Install Dependencies
Updated `pyproject.toml` to include `requests`, `beautifulsoup4`, and `gradio`.

```bash
poetry install
```

(This installs all dependencies, including the new ones.)

### 2. Verify .env
Make sure `.env` has your Groq API key:
```
GROQ_API_KEY=gsk_...
```

## Running the Pipeline

### Step 1: Ingest Documents
Scrapes all 10 source URLs, extracts clean text, chunks semantically, saves JSON files to `documents/`.

```bash
poetry run python ingest.py
```

**Expected output:**
- 50–150 JSON files in `documents/` directory
- Each file named `chunk_0000.json`, `chunk_0001.json`, etc.
- Each chunk is 1000–1500 characters
- Includes section headings for context

**Spot-check:**
```bash
python3 -c "import json; d=json.load(open('documents/chunk_0000.json')); print(f\"Chars: {d['char_count']}\nSource: {d['source_url']}\")"
```

---

### Step 2: Embed & Store
Embeds all chunks using `all-mpnet-base-v2`, stores in ChromaDB persisted to `chroma_db/`.

```bash
poetry run python embed.py
```

**Expected output:**
```
Loaded N chunks from documents
Initializing embedding model: all-mpnet-base-v2
Initializing ChromaDB (persisted to chroma_db)
Encoding N chunks...
Upserting to ChromaDB collection 'benefits_guide'...
✓ Collection now has N documents
```

**Note:** First run takes ~30 seconds (downloads model). Subsequent runs are instant.

---

### Step 3: Query via Gradio Web UI
Launches a web interface at `http://127.0.0.1:7860`. Type questions, get grounded answers + sources.

```bash
poetry run python query.py
```

**Then open your browser to `http://127.0.0.1:7860`**

---

## Testing the Full Pipeline

Test with your 6 evaluation questions:

1. **"Why should someone choose to max out their medical FSA account?"**
   - Expected: Mentions "use-it-or-lose-it" rule, predictable expenses, tax advantages, grace period/carryover
   - Sources: TurboTax, Anders CPA

2. **"If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth?"**
   - Expected: Must stay until vesting, unvested shares forfeited if you leave, vested shares are yours
   - Sources: Woven Capital

3. **"If I am already covered for health insurance, should I even consider enrolling in my company's plan?"**
   - Expected: Yes, better coverage/lower costs, employer contributions to HSA/FSA
   - Sources: Multiple sources (might be limited since this is not directly covered)

4. **"What is open enrollment?"**
   - Expected: Annual period for changing benefits, outside of it requires qualifying life event
   - Sources: Anders CPA, TurboTax

5. **"What is the difference between PTO, short-term disability, and long-term disability?"**
   - Expected: PTO is discretionary time off, STD replaces salary weeks-to-months, LTD for longer-term
   - Sources: Anders CPA, MetLife

6. **"What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket?"**
   - Expected: Pre-tax deductions, often rollover (unlike medical FSA), saves on taxes
   - Sources: Randstad

---

## Troubleshooting

### "GROQ_API_KEY not set in .env file"
Make sure `.env` exists in the project root with:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### "No chunk_*.json files found in documents"
Run `poetry run python ingest.py` first to scrape and chunk the sources.

### "Directory chroma_db not found"
Run `poetry run python embed.py` to build the ChromaDB collection.

### Model download hangs
First run of `embed.py` downloads the embedding model (~420MB). It requires internet access. Subsequent runs use the cached model.

### Reddit wiki returns insufficient content
The Reddit wiki URL (`/wiki/commontopics`) is a wiki page that may be scraped differently. The script will warn and skip it if it returns <200 chars of useful text. This is graceful degradation — the system works fine with 9 sources.

---

## Pipeline Diagram

```
ingest.py (fetches 10 URLs)
    ↓
documents/*.json (50-150 chunks saved)
    ↓
embed.py (encodes with all-mpnet-base-v2, stores in ChromaDB)
    ↓
chroma_db/ (persistent vector database)
    ↓
query.py (Gradio UI)
    ↓
(on user query) retrieve(query) → retrieve top-3 chunks
    ↓
format context + system prompt
    ↓
Groq API (llama-3.3-70b-versatile) → grounded answer
    ↓
Display answer + sources in Gradio UI
```

---

## File Structure After Full Run

```
ai201-project1-unofficial-guide-starter/
├── ingest.py
├── embed.py
├── query.py
├── documents/
│   ├── chunk_0000.json
│   ├── chunk_0001.json
│   └── ... (50-150 files)
├── chroma_db/
│   ├── chroma.sqlite3
│   └── (other ChromaDB internal files)
├── pyproject.toml (updated)
├── .env (has GROQ_API_KEY)
└── planning.md (your spec)
```
