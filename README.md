# Qdrant Vector Database Demo

This repository contains a small working demonstration of **Qdrant**, an open-source vector database built for similarity search. The example shows how to create a collection, insert vectors with metadata, and run a filtered semantic-style search using Qdrant in Docker.

## 1. What is this tool?
Qdrant is a vector database and similarity search engine written in Rust. It stores numeric vector embeddings together with payload fields such as category, tags, or year, then retrieves the closest matches using distance metrics like cosine similarity.

## 2. Prerequisites
- Linux, macOS, or Windows with WSL2
- Docker Engine
- Docker Compose
- Python 3.10+ and `pip`

## 3. Installation
1. Clone your repository:

```bash
git clone https://github.com/hazarsozer/qdrant-demo.git
cd tool-representation
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Start Qdrant:

```bash
docker compose up -d
```

5. Optional: review environment settings:

```bash
cat .env.example
```

The demo reads `QDRANT_HOST` and `QDRANT_PORT` from environment variables if you choose to set them.

## 4. Running the Example
Run the demo script:

```bash
python3 demo.py
```

What the script does:
- Creates a collection named `tech_books`
- Generates a small deterministic vector for each book title
- Uploads the vectors and metadata payloads to Qdrant
- Searches for a query using cosine similarity
- Applies a metadata filter so only `category="coding"` results are returned

## 5. Expected Output
Example terminal output:

```text
Creating collection: tech_books...
Upserting data into Qdrant...
Successfully upserted 4 points.

Searching for: 'programming and software development' with category filter 'coding'...
Search Results:
 - [Score: 0.2923] Introduction to Rust Programming (Year: 2021)
 - [Score: 0.1983] Machine Learning with Python (Year: 2022)
```

You can also open the Qdrant dashboard in your browser:

```text
http://localhost:6333/dashboard
```

Note on embeddings:
This classroom demo uses a lightweight deterministic embedding function implemented in `demo.py` so the repository stays small and runs without downloading a large ML model. In a production system, Qdrant would usually store embeddings produced by a real model such as Sentence Transformers, OpenAI embeddings, or another encoder.

## 6. AI Usage Disclosure
The repository was prepared with AI assistance and then reviewed manually.

- Gemini was used earlier for planning, outline generation, and initial draft materials.
- Codex was used to review the repository, simplify the demo, improve reproducibility, and rewrite the documentation and presentation materials.

All code and text should be reviewed by the student before submission and presentation.
