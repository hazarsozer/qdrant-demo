import os

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

COLLECTION_NAME = "tech_books"
VECTOR_SIZE = 384
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

print("Loading embedding model...")
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> list[float]:
    return _model.encode(text).tolist()


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


def search(client: QdrantClient, query_text: str) -> None:
    print(f"\nSearching for: '{query_text}'...")

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_text(query_text),
        limit=4,
    )

    print("Results:")
    for result in response.points:
        print(
            f" - [Score: {result.score:.4f}] "
            f"{result.payload['title']} [{result.payload['category']}] ({result.payload['year']})"
        )


def main() -> None:
    client = build_client()
    setup_collection(client)
    upsert_data(client)

    print("\nQdrant ready. Type a query to search (Ctrl+C to stop).")
    while True:
        try:
            query = input("\nQuery: ").strip()
            if query:
                search(client, query)
        except KeyboardInterrupt:
            print("\nDone.")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}")
        print("\nMake sure Qdrant is running: docker compose up -d")
