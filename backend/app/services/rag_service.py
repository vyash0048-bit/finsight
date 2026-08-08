import datetime
import logging
import os


from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

_cross_encoder = None
_embedding_func = None
_chroma_client = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        import chromadb
        chroma_path = os.getenv("CHROMA_PATH", ".cache/chroma")
        try:
            os.makedirs(chroma_path, exist_ok=True)
        except PermissionError:
            logger.warning(f"Permission denied when creating {chroma_path}. Falling back to '.cache/chroma'.")
            chroma_path = ".cache/chroma"
            os.makedirs(chroma_path, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=chroma_path)
    return _chroma_client

def get_embedding_func():
    global _embedding_func
    if _embedding_func is None:
        from chromadb.utils import embedding_functions
        _embedding_func = embedding_functions.DefaultEmbeddingFunction()
    return _embedding_func

def get_cross_encoder():
    global _cross_encoder
    if _cross_encoder is None:
        try:
            from sentence_transformers import CrossEncoder
            _cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)
        except Exception as e:
            logger.warning(f"Could not load cross_encoder: {e}")
    return _cross_encoder

def get_collection(collection_name: str = "news"):
    return get_chroma_client().get_or_create_collection(
        name=collection_name,
        embedding_function=get_embedding_func()
    )

def chunk_text(text: str) -> list[str]:
    """
    Helper function to chunk text respecting paragraphs and sentences.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def ingest(document: dict, collection_name: str = "news") -> int:
    """
    Ingests a document into ChromaDB.
    
    document should have:
    - id (str): Unique document identifier.
    - text (str): The text content of the document.
    - metadata (dict): Metadata including ticker, source, date, url.
    """
    collection = get_collection(collection_name)
    
    text = document.get("text", "")
    doc_id = document.get("id", "doc_id")
    metadata = document.get("metadata", {})
    
    chunks = chunk_text(text)
    
    if not chunks:
        return 0
        
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [metadata for _ in chunks]
    
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    
    return len(chunks)

def retrieve(query: str, ticker: str = None, k: int = 3, collection_name: str = "news"):
    """
    Retrieves the top k most relevant chunks for a given query, optionally filtered by ticker.
    """
    collection = get_collection(collection_name)
    
    where_clause = None
    if ticker:
        where_clause = {"ticker": ticker}
        
    results = collection.query(
        query_texts=[query],
        n_results=k,
        where=where_clause
    )
    
    return results

def retrieve_and_rerank(query: str, ticker: str = None, k: int = 3, collection_name: str = "news"):
    """
    Retrieves the top k*5 candidates and reranks them using a cross-encoder to return the best k.
    """
    # Fetch more candidates for reranking
    initial_k = k * 5
    results = retrieve(query, ticker=ticker, k=initial_k, collection_name=collection_name)
    
    ce = get_cross_encoder()
    if not results or not results["documents"] or not results["documents"][0] or ce is None:
        return results
        
    docs = results["documents"][0]
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    
    # Create pairs of (query, document) for the cross encoder
    pairs = [[query, doc] for doc in docs]
    
    # Predict relevance scores
    scores = ce.predict(pairs)
    
    # Pair up the scores with the results and sort descending by score
    scored_docs = list(zip(scores, ids, docs, metadatas))
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # Get top k
    top_k = scored_docs[:k]
    
    reranked_results = {
        "ids": [[item[1] for item in top_k]],
        "documents": [[item[2] for item in top_k]],
        "metadatas": [[item[3] for item in top_k]],
        "distances": [[item[0] for item in top_k]] # Returning scores instead of distances
    }
    
    return reranked_results

def delete_stale_documents(days_old: int = 30, collection_name: str = "news"):
    """
    TTL Strategy: Deletes documents older than `days_old` days.
    Relies on the date being stored in metadata as 'YYYY-MM-DD'.
    """
    collection = get_collection(collection_name)
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d")
    
    try:
        collection.delete(
            where={"date": {"$lt": cutoff_date}}
        )
        logger.info(f"Deleted documents older than {cutoff_date} from {collection_name}")
    except Exception as e:
        logger.error(f"Failed to delete stale documents: {e}")
