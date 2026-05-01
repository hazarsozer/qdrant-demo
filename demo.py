import hashlib
import math
import os

from qdrant_client import QdrantClient
from qdrant_client.http import models

COLLECTION_NAME = "tech_books"
VECTOR_SIZE = 8
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))


def tokenize(text: str) -> list[str]:
    cleaned = text.lower().replace("-", " ")
    return [token for token in cleaned.split() if token]


def embed_text(text: str) -> list[float]:
    # Lightweight deterministic embedding for a classroom demo.
    # It simulates turning text into vectors without external model downloads.
    vector = [0.0] * VECTOR_SIZE

    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        bucket = digest[0] % VECTOR_SIZE
        sign = 1.0 if digest[1] % 2 == 0 else -1.0
        weight = 1.0 + (digest[2] / 255.0)
        vector[bucket] += sign * weight

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector

    return [value / norm for value in vector]


def build_client() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def setup_collection(client: QdrantClient) -> None:
    print(f"Creating collection: {COLLECTION_NAME}...")
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE,
        ),
    )


def sample_documents() -> list[dict]:
    return [
        {
            "id": 1,
            "title": "Introduction to Rust Programming",
            "category": "coding",
            "year": 2021,
        },
        {
            "id": 2,
            "title": "Advanced Data Engineering Patterns",
            "category": "data",
            "year": 2023,
        },
        {
            "id": 3,
            "title": "Vector Databases for Beginners",
            "category": "databases",
            "year": 2024,
        },
        {
            "id": 4,
            "title": "Machine Learning with Python",
            "category": "coding",
            "year": 2022,
        },
    ]


def upsert_data(client: QdrantClient) -> None:
    print("Upserting data into Qdrant...")
    documents = sample_documents()

    points = [
        models.PointStruct(
            id=doc["id"],
            vector=embed_text(doc["title"]),
            payload=doc,
        )
        for doc in documents
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Successfully upserted {len(points)} points.")


def search_with_filter(client: QdrantClient, query_text: str) -> None:
    print(f"\nSearching for: '{query_text}' with category filter 'coding'...")

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_text(query_text),
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(value="coding"),
                )
            ]
        ),
        limit=2,
    )

    print("Search Results:")
    for result in response.points:
        print(
            f" - [Score: {result.score:.4f}] "
            f"{result.payload['title']} (Year: {result.payload['year']})"
        )


def main() -> None:
    client = build_client()
    setup_collection(client)
    upsert_data(client)
    search_with_filter(client, "programming and software development")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}")
        print("\nMake sure Qdrant is running: docker compose up -d")
