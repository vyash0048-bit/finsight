import pytest
import os
from app.services.rag_service import chunk_and_store_text, search_similar_text

def test_chunk_and_store_text():
    text = "The Federal Reserve raised interest rates by 25 basis points today. Markets reacted positively across all sectors."
    metadata = {"source": "test_news", "ticker": "SPY"}
    
    num_chunks = chunk_and_store_text("test_doc_1", text, metadata, collection_name="test_news_collection")
    assert num_chunks > 0
    
    results = search_similar_text("Did the fed raise rates?", n_results=1, collection_name="test_news_collection")
    
    assert results is not None
    assert len(results["documents"][0]) > 0
    assert "Federal Reserve" in results["documents"][0][0]
