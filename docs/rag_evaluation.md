# Phase 9: Vector Database Hardening & Evaluation

## Design Decisions

### 1. Single Collection with Metadata Filtering vs Collection-per-Ticker
We chose a **Single Collection with Metadata Filtering** design.
- **Why?** A single collection (`"news"`) reduces the overhead of creating and managing thousands of collections (one for each ticker symbol). ChromaDB supports highly efficient boolean and inequality filtering on metadata fields. We store `"ticker"` in the document metadata, enabling us to easily scope any query to a specific ticker via the `.query(where={"ticker": "AAPL"})` syntax.

### 2. Retrieval Optimization: Lightweight Reranking
- **Why?** Naive semantic search using bi-encoders (like the sentence-transformers default) often suffers when query-document relationships rely on subtle semantic nuances rather than pure lexical similarity. Running a full LLM (e.g. GPT-4) on every retrieved chunk is incredibly slow and expensive.
- **Solution?** We introduced a two-pass retrieval system using a lightweight Cross-Encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`).
  - *Pass 1:* Retrieve the top `k * 5` candidates quickly using the base vector embeddings.
  - *Pass 2:* Run the candidates through the Cross-Encoder to predict true relevance and rerank them, then return the definitive top `k`.

### 3. TTL / Refresh Strategy
- **Why?** Financial news loses relevancy quickly; holding onto multi-year old news clutters the semantic space.
- **Solution?** We implemented a TTL function (`delete_stale_documents(days_old)`) that programmatically drops documents older than a specified threshold (e.g., 30 days) using ChromaDB's `<` conditional filtering on the `date` metadata field.

## Before/After Retrieval Example

**Evaluation Setup:**
We inserted 5 news items regarding Apple and Microsoft. One document contained the true answer, while others served as semantic distractors.

**Query:** `"What drove Apple's record Q3 revenues?"`

- **Naive Retrieval Top Doc (Before):**
  > "Investors are closely watching Apple's Q3 revenue breakdown, specifically looking at iPhone sales numbers which represent the core business." *(A distractor doc sharing similar keywords but not answering the question).*
  
- **Reranked Retrieval Top Doc (After Cross-Encoder):**
  > "Apple reported record revenues in Q3 driven primarily by strong iPhone 15 sales across emerging markets." *(The correct document containing the factual answer).*

This demonstrates the measurable improvement in precision@k (k=1) when combining fast bi-encoder candidate generation with accurate cross-encoder scoring.
