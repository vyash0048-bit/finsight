import pytest
import datetime
from app.services.rag_service import ingest, retrieve

def test_chunk_and_store():
    # Simple test for basic chunking/storage logic
    document = {
        "id": "test_1",
        "text": "This is a test document. It has multiple sentences. We will test the RAG ingestion.",
        "metadata": {"ticker": "TEST", "date": datetime.datetime.now().strftime("%Y-%m-%d")}
    }
    num_chunks = ingest(document, collection_name="test_collection")
    assert num_chunks > 0

def test_search_similar():
    document = {
        "id": "test_2",
        "text": "Apple announced a new iPhone today.",
        "metadata": {"ticker": "AAPL", "date": datetime.datetime.now().strftime("%Y-%m-%d")}
    }
    ingest(document, collection_name="test_collection")
    
    results = retrieve("iPhone announcement", ticker="AAPL", k=1, collection_name="test_collection")
    
    assert results is not None
    assert "documents" in results
    assert len(results["documents"]) > 0
    assert "Apple" in results["documents"][0][0]
