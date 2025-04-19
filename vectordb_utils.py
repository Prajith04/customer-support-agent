# vectordb_utils.py

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import uuid
import os

# Setup cache dir
cache_dir = os.environ.get("MODEL_CACHE_DIR", "/app/cache")  # Fallback
os.makedirs(cache_dir, exist_ok=True)

# Encoder and Qdrant config
encoder = SentenceTransformer("all-MiniLM-L6-v2", cache_folder=cache_dir)
qdrant = QdrantClient(":memory:")
collection_name = "customer_support_docsv1"

# Initialize collection
def init_qdrant_collection():
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

# Add a query/response to DB
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

# Search DB
def search_vectordb(query, limit=3):
    vector = encoder.encode(query).tolist()
    return qdrant.search(collection_name=collection_name, query_vector=vector, limit=limit)

# 🆕 Load and populate from Hugging Face dataset
def populate_vectordb_from_hf():
    print("Loading dataset from Hugging Face...")
    dataset = load_dataset("Talhat/Customer_IT_Support", split="train")

    print("Populating vector DB...")
    for item in dataset:
        query = item.get("body", "").strip()
        response = item.get("answer", "").strip()
        if query and response:
            add_to_vectordb(query, response)

    print("Vector DB population complete.")
