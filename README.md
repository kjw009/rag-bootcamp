# RAG Bootcamp Notebooks

Six Jupyter notebooks matching the 5-day bootcamp + a Day 0 setup notebook.
All code is framework-free (no LangChain, no LlamaIndex) so consultants learn
the primitives first.

## Contents

| File | Day | Purpose |
|------|-----|---------|
| `day0_setup.ipynb` | Day 0 | Environment check, API key test, corpus download |
| `day1_naive_rag.ipynb` | Day 1 | End-to-end RAG from primitives, MiniLM + OpenAI embeds, Chroma, Claude |
| `day2_parsing_ocr.ipynb` | Day 2 | Diagnostic on cursed pack, Tesseract + OpenCV deskew, Docling for tables/bullets |
| `day3_chunking_metadata.ipynb` | Day 3 | Fixed vs recursive vs semantic chunking, LLM metadata extraction, filtered retrieval |
| `day4_scraping_retrieval.ipynb` | Day 4 | Responsible scraping, BM25 + dense hybrid with RRF, cross-encoder reranking, Ragas |
| `day5_capstone.ipynb` | Day 5 | Capstone template — teams fill in for real client data |
| `utils.py` | all | Shared helpers — LLM client, Chunk dataclass, Chroma helpers, eval |

## Setup

Place these alongside `cursed_pack/` (from the PDF pack I shared earlier):

```
project/
├── notebooks/           ← you are here
│   ├── utils.py
│   ├── day0_setup.ipynb
│   └── ...
├── cursed_pack/
│   ├── 01_multipage_table_of_doom.pdf
│   ├── 02_nested_bullet_nightmare.pdf
│   ├── 03_layout_monster.pdf
│   └── 04_skewed_scan.pdf
├── datasets/
│   ├── day1/            ← populated by day0_setup.ipynb
│   └── client/          ← populated by instructor on Day 5
└── .env                 ← contains ANTHROPIC_API_KEY
```

Then start with `day0_setup.ipynb` — it installs dependencies, tests API
keys, and downloads the Day 1 PEP corpus.

## System dependencies (install once per machine)

Outside `pip`, you need:

- **Tesseract OCR** — `brew install tesseract` / `apt install tesseract-ocr`
- **Poppler** — `brew install poppler` / `apt install poppler-utils`
- Optional: `playwright install chromium` if you'll do dynamic scraping

## API key

The notebooks default to Claude (Anthropic). Create `.env` with:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...      # optional, enables Day 1 embedding comparison
```

To swap to OpenAI as the main LLM, see the commented block in `utils.py` —
it's a 10-line change.

## Design notes for the instructor

**Why framework-free?** Consultants who only know LangChain are fragile on
client engagements. Everything in LangChain and LlamaIndex is built on the
primitives these notebooks use. Once consultants know the primitives, picking
up a framework is 30 minutes. The reverse is not true.

**Why Claude instead of OpenAI?** Personal preference — Sonnet 4.5 is strong
for grounded Q&A and the Anthropic SDK is clean. The code swaps to OpenAI in
two lines if you prefer.

**Why local embeddings (MiniLM) as the default?** Free, fast, good enough for
Day 1–3 exploration. Day 3 compares against BGE-large and OpenAI. In real
engagements, start with MiniLM, escalate only when evaluation shows you need to.

**Why local reranking (bge-reranker-base)?** Cohere Rerank is great but adds
an external API dependency. The bge-reranker is ~280MB, runs on CPU in
acceptable time, and is free. Use Cohere in production if budget allows.

**Why Docling and not LlamaParse or Unstructured?** Docling is free, actively
maintained (IBM), handles layout and tables well, and has no rate limits.
Unstructured is good but has more moving parts. LlamaParse is paid. On
Day 2 we teach all three categories but default to Docling for the exercises.

## Known gotchas

1. **BGE-large-en-v1.5 is a 1.3GB download.** The eval cell that uses it is
   commented out by default. Uncomment when you're ready.
2. **bge-reranker-base is 280MB and first-load takes ~30 seconds.** Don't
   reset the kernel mid-exercise.
3. **Ragas ≥ 0.2 changed its API.** The Day 4 Ragas cells are commented with
   the canonical shape — uncomment and adjust to your installed version.
4. **The Day 4 scraping target (python.org/events) may change its HTML
   structure.** If the selector `ul.list-recent-events li` breaks, teams
   should diagnose it — that's a realistic scraping lesson.
5. **Day 5 `capstone` is a template**. Teams must fill in `parse_client_file()`,
   the eval set, and the production checklist — those blanks are the point.

## File sizes

All notebooks are under 25KB. The `utils.py` is 150 lines, readable in one
sitting.

## Running order

Strictly linear. Each day depends on collections created by the previous day.
If a consultant skips a day and asks why things don't work, that's the
lesson.
