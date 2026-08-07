import logging
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os

logger = logging.getLogger(__name__)

# Initialize ChromaDB in persistent mode
chroma_path = os.getenv("CHROMA_PATH", "/app/.cache/chroma")
os.makedirs(chroma_path, exist_ok=True)
client = chromadb.PersistentClient(path=chroma_path)

# Default embedding function uses all-MiniLM-L6-v2 via onnx
embedding_func = embedding_functions.DefaultEmbeddingFunction()

def get_collection(collection_name: str = "news"):
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_func
    )

def chunk_and_store_text(doc_id: str, text: str, metadata: dict, collection_name: str = "news") -> int:
    """
    Very simple chunking and storing for text data.
    """
    collection = get_collection(collection_name)
    
    # Simple chunking by paragraph or fixed length
    # For demonstration, we just split by 1000 characters
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [metadata for _ in chunks]
    
    if chunks:
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
    return len(chunks)

def search_similar_text(query: str, n_results: int = 3, collection_name: str = "news"):
    collection = get_collection(collection_name)
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
