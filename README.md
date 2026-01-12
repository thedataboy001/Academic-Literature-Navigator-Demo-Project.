# Academic Literature Navigator

A small research assistant for indexing and exploring academic papers using embeddings, FAISS, and an LLM-powered RAG workflow. The project includes tools to parse PDFs (via GROBID), chunk text, build a FAISS index, and run interactive exploration via Streamlit and notebooks.

**Key features:**
- Index PDFs into a FAISS vector store using OpenAI embeddings.
- Run retrieval-augmented generation (RAG) with a Chat LLM.
- Parse PDFs to TEI XML using a local GROBID instance and convert to plain text.
- Example exploratory notebook and a small Streamlit app for demos.

**Prerequisites**
- Python 3.10+ (Windows tested)
- Docker (for running GROBID locally) or a reachable GROBID server
- An OpenAI-compatible API key set in a `.env` file for embeddings/LLM usage

## Quick setup

1. Create a virtual environment and install dependencies (example):

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\\Scripts\\activate
pip install -U pip
pip install -r requirements.txt
```

2. Create a `.env` file at the project root with your API key(s):

```text
OPENAI_API_KEY=sk-...
# any other env vars your local setup requires
```

3. Start a local GROBID instance (optional, recommended for PDF parsing):

```bash
docker run -p 8070:8070 lfoppiano/grobid:0.7.2
```

## Running the project

- Run the Streamlit demo (simple UI):

```bash
streamlit run streamlit.py
```

- Open the exploratory notebook: [notebooks/eda.ipynb](notebooks/eda.ipynb)

## How the pieces fit

- `papers/` — source PDFs and the saved FAISS index folder at `papers/papers_index`.
- `notebooks/eda.ipynb` — end-to-end demonstration: parse PDF with GROBID, convert TEI→text, chunk text, embed, build FAISS, and run RAG queries.
- `src/app.py` — application entry (auxiliary app code).
- `src/rag.py`, `src/parse_functions.py`, `src/txt_chunk_functions.py`, `src/helper_functions.py` — helper modules used by the notebook and app for parsing, chunking, vector store creation, and RAG orchestration.
- `streamlit.py` — lightweight demo UI (run with `streamlit run streamlit.py`).

## Typical workflow

1. Place or download a paper PDF into `papers/`.
2. Use the notebook or `src` utilities to parse the PDF (GROBID) and convert TEI XML to plain text.
3. Chunk the text and create `Document` objects.
4. Embed chunks using OpenAI embeddings and build a FAISS index (`papers/papers_index`).
5. Create a retriever and run RAG prompts with the LLM.

## Notes & troubleshooting

- If GROBID is unreachable, ensure the Docker container is running and reachable at `http://localhost:8070` (this URL can be found/changed in the notebook).
- Embedding and LLM calls require an OpenAI-compatible key; set it in `.env` and ensure the environment is loaded (the notebook uses `dotenv.load_dotenv()`).
- FAISS index files are saved to `papers/papers_index` by the example notebook — back these up if reindexing.

## Next steps

- `requirements.txt` is included for reproducible installs.
- Add a small CLI for indexing multiple PDFs.
- Provide Streamlit UI controls for reindexing and query examples.

---

## Contributing
Improvements are welcome. Open an issue or submit a PR with focused changes.

## License
This project is licensed under the MIT License — see [LICENSE](LICENSE) for the full text.

Copyright (c) 2026 Stephen Elufisan (Thedataboy)