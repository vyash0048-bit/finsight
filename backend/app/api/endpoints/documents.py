import hashlib
import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.deps import get_current_user
from app.models.user import User
from app.services.rag_service import ingest, retrieve, retrieve_and_rerank

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class IngestRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker (e.g. 'AAPL')")
    text: str = Field(..., min_length=10, description="Document text content to embed")
    source: str = Field("manual", description="Source identifier")
    url: str = Field("", description="Optional source URL")


class IngestResponse(BaseModel):
    chunks_added: int
    document_id: str


class SearchResult(BaseModel):
    id: str
    text: str
    metadata: dict[str, Any]
    score: float | None = None


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/ingest", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
def ingest_document(
    body: IngestRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Manually ingest and embed a document into the ChromaDB vector store.
    """
    ticker = body.ticker.strip().upper()

    # Deterministic document ID from ticker + text hash
    text_hash = hashlib.sha256(body.text.encode()).hexdigest()[:12]
    doc_id = f"{ticker}_{text_hash}"

    metadata = {
        "ticker": ticker,
        "source": body.source,
        "url": body.url,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

    document = {
        "id": doc_id,
        "text": body.text,
        "metadata": metadata,
    }

    try:
        chunks_added = ingest(document, collection_name="news")
    except Exception as e:
        logger.error(f"Ingestion failed for {ticker}: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document ingestion failed: {e!s}",
        )

    logger.info(f"User {current_user.id} ingested doc {doc_id} — {chunks_added} chunks")

    return IngestResponse(chunks_added=chunks_added, document_id=doc_id)


@router.get("/search", response_model=SearchResponse)
def search_documents(
    query: str = Query(..., min_length=1, description="Search query"),
    ticker: str = Query(None, description="Optional ticker filter"),
    k: int = Query(3, ge=1, le=20, description="Number of results to return"),
    rerank: bool = Query(True, description="Whether to use cross-encoder reranking"),
    current_user: User = Depends(get_current_user),
):
    """
    Query the ChromaDB vector store directly.
    Useful for debugging agent retrieval logic.
    """
    if ticker:
        ticker = ticker.strip().upper()

    try:
        if rerank:
            raw_results = retrieve_and_rerank(query, ticker=ticker, k=k, collection_name="news")
        else:
            raw_results = retrieve(query, ticker=ticker, k=k, collection_name="news")
    except Exception as e:
        logger.error(f"Vector search failed: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {e!s}",
        )

    # Parse ChromaDB results into response model
    results: list[SearchResult] = []

    if raw_results and raw_results.get("documents") and raw_results["documents"][0]:
        ids = raw_results.get("ids", [[]])[0]
        docs = raw_results["documents"][0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        distances = raw_results.get("distances", [[]])[0]

        for i, doc_text in enumerate(docs):
            results.append(SearchResult(
                id=ids[i] if i < len(ids) else f"result_{i}",
                text=doc_text,
                metadata=metadatas[i] if i < len(metadatas) else {},
                score=float(distances[i]) if i < len(distances) else None,
            ))

    return SearchResponse(query=query, results=results)
