# vectordb_utils.py

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
cache_dir = os.environ.get("MODEL_CACHE_DIR", "/app/cache")  # Fallback to /app/cache
os.makedirs(cache_dir, exist_ok=True)
encoder =SentenceTransformer("all-MiniLM-L6-v2", cache_folder=cache_dir)
qdrant = QdrantClient(":memory:")
collection_name = "customer_support_docsv1"

def init_qdrant_collection():
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

def add_to_vectordb(query, response):
    vector = encoder.encode(query).tolist()
    qdrant.upload_points(
        collection_name=collection_name,
        points=[PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"query": query, "response": response}
        )]
    )

def search_vectordb(query, limit=3):
    vector = encoder.encode(query).tolist()
    return qdrant.search(collection_name=collection_name, query_vector=vector, limit=limit)
