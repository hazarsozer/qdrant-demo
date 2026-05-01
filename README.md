# Qdrant Vector Database Demo

This repository contains a small working demonstration of **Qdrant**, an open-source vector database built for similarity search. The example shows how to create a collection, insert vectors with metadata, and run interactive semantic search queries using Qdrant in Docker and sentence-transformers embeddings.

## 1. What is this tool?
Qdrant is a vector database and similarity search engine written in Rust. It stores numeric vector embeddings together with payload fields such as category, tags, or year, then retrieves the closest matches using distance metrics like cosine similarity. It is commonly used for semantic search, recommendation systems, and retrieval in AI pipelines.

## 2. Prerequisites
- Linux, macOS, or Windows with WSL2
- Docker Engine and Docker Compose
- Python 3.10+ and `pip`

## 3. Installation
1. Clone the repository:

```bash
git clone https://github.com/hazarsozer/qdrant-demo.git
cd qdrant-demo
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\Activate.ps1    # Windows PowerShell
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

> Note: `sentence-transformers` will download the `all-MiniLM-L6-v2` model (~80 MB) on first run. It is cached locally after that.

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
- Loads the `all-MiniLM-L6-v2` sentence-transformers model locally
- Creates a collection named `tech_books` with 384-dimensional vectors
- Embeds each book title using the model and uploads the vectors with metadata payloads to Qdrant
- Enters an interactive loop where you can type any query and receive ranked similarity results

## 5. Expected Output

```text
Loading embedding model...
Creating collection: tech_books...
Upserting data into Qdrant...
Successfully upserted 4 points.

Qdrant ready. Type a query to search (Ctrl+C to stop).

Query: python machine learning

Searching for: 'python machine learning'...
Results:
 - [Score: 0.9663] Machine Learning with Python [coding] (2022)
 - [Score: 0.3386] Vector Databases for Beginners [databases] (2024)
 - [Score: 0.2054] Advanced Data Engineering Patterns [data] (2023)
 - [Score: 0.1665] Introduction to Rust Programming [coding] (2021)

Query: data engineering patterns

Searching for: 'data engineering patterns'...
Results:
 - [Score: 0.9400] Advanced Data Engineering Patterns [data] (2023)
 - [Score: 0.3575] Vector Databases for Beginners [databases] (2024)
 - [Score: 0.2431] Introduction to Rust Programming [coding] (2021)
 - [Score: 0.2124] Machine Learning with Python [coding] (2022)
```

You can also open the Qdrant dashboard in your browser:

```
http://localhost:6333/dashboard
```

## 6. AI Usage Disclosure
The repository was prepared with AI assistance and then reviewed manually.

- Gemini was used earlier for planning, outline generation, and initial draft materials.
- Codex was used to review the repository, simplify the demo, improve reproducibility, and rewrite the documentation and presentation materials.
- Claude was used to debug the setup, upgrade the embedding from a placeholder SHA256 function to sentence-transformers, and extend the demo to support interactive queries.

All code and text was reviewed by the student before submission and presentation.
