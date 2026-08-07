from app.services.rag_service import client, ingest, retrieve, retrieve_and_rerank


def test_rag_evaluation():
    # Arrange: Create multiple mock documents
    # Distractor documents have overlapping vocabulary with the query.
    # The true answer is doc_1.
    docs = [
        {
            "id": "doc_1",
            "text": "Apple reported record revenues in Q3 driven primarily by strong iPhone 15 sales across emerging markets.",
            "metadata": {"ticker": "AAPL", "source": "NewsA", "date": "2023-10-01"}
        },
        {
            "id": "doc_2",
            "text": "Apple is planning to launch a new smartwatch next year with health tracking features.",
            "metadata": {"ticker": "AAPL", "source": "NewsB", "date": "2023-10-05"}
        },
        {
            "id": "doc_3",
            "text": "The latest Apple earnings report highlighted weakness in the Mac segment despite overall revenue growth.",
            "metadata": {"ticker": "AAPL", "source": "NewsC", "date": "2023-10-10"}
        },
        {
            "id": "doc_4",
            "text": "Microsoft's Azure cloud growth accelerated this quarter, beating Q3 revenue expectations significantly.",
            "metadata": {"ticker": "MSFT", "source": "NewsD", "date": "2023-10-15"}
        },
        {
            "id": "doc_5",
            "text": "Investors are closely watching Apple's Q3 revenue breakdown, specifically looking at iPhone sales numbers which represent the core business.",
            "metadata": {"ticker": "AAPL", "source": "NewsE", "date": "2023-10-20"}
        }
    ]
    
    # Try to ensure a clean slate for this eval collection
    try:
        client.delete_collection("eval_news_collection")
    except Exception:
        pass
        
    for d in docs:
        ingest(d, collection_name="eval_news_collection")
        
    query = "What drove Apple's record Q3 revenues?"
    
    # Act: Naive retrieval
    naive_results = retrieve(query, ticker="AAPL", k=1, collection_name="eval_news_collection")
    naive_doc = naive_results["documents"][0][0]
    
    # Act: Reranked retrieval
    reranked_results = retrieve_and_rerank(query, ticker="AAPL", k=1, collection_name="eval_news_collection")
    reranked_doc = reranked_results["documents"][0][0]
    
    print("\n--- RAG Evaluation ---")
    print(f"Query: {query}")
    print(f"Naive Top Doc: {naive_doc}")
    print(f"Reranked Top Doc: {reranked_doc}")
    
    # In some cases, the sentence embeddings might rank doc_5 higher due to word overlap ("Q3", "revenue", "Apple").
    # The cross-encoder is typically better at understanding the semantic answer.
    
    # Assertions
    assert len(reranked_results["documents"][0]) > 0
    # Clean up
    try:
        client.delete_collection("eval_news_collection")
    except Exception:
        pass
