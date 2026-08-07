import pytest
from app.services.rag_service import ingest, retrieve

def test_rag_integration_ingest_and_retrieve():
    # Arrange: Create a mock document with known facts
    doc = {
        "id": "test_news_123",
        "text": "Tesla has announced the new Model Pi smartphone. It features Starlink integration and solar charging capabilities. It is expected to revolutionize the market.",
        "metadata": {
            "ticker": "TSLA",
            "source": "TechCrunch",
            "date": "2023-11-01",
            "url": "https://example.com/tesla-pi"
        }
    }
    
    # Act: Ingest document
    num_chunks = ingest(doc, collection_name="test_integration_news")
    
    # Assert ingestion success
    assert num_chunks > 0, "Document should be chunked and ingested."
    
    # Act: Retrieve known fact
    query = "What features does the new Tesla smartphone have?"
    results = retrieve(query, ticker="TSLA", k=1, collection_name="test_integration_news")
    
    # Assert retrieval
    assert results is not None
    assert "documents" in results
    assert len(results["documents"][0]) > 0, "Should retrieve at least one document chunk"
    
    # Check if the retrieved chunk contains the fact
    retrieved_text = results["documents"][0][0]
    assert "Starlink integration" in retrieved_text or "solar charging" in retrieved_text or "Model Pi" in retrieved_text
    
    # Also verify metadata is preserved
    metadatas = results["metadatas"][0][0]
    assert metadatas["ticker"] == "TSLA"
    assert metadatas["source"] == "TechCrunch"
