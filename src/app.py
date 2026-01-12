from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import tempfile
import os

from langchain_core.documents import Document

from src.txt_chunk_functions import text_to_chunks
from src.rag import build_rag_chain

app = FastAPI(title="Academic Literature Navigator")

# -------------------------
# In-memory document store
# (Replace with Redis / DB later)
# -------------------------
DOCUMENT_STORE: Dict[str, List[Document]] = {}


# -------------------------
# Request / Response Models
# -------------------------
class QuestionRequest(BaseModel):
    document_id: str
    question: str
    k: int = 8
    fetch_k: int = 20


class AnswerResponse(BaseModel):
    answer: str


# -------------------------
# Upload PDF Endpoint
# -------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF papers are supported.")

    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Convert PDF → chunks
        documents = text_to_chunks(tmp_path)

        if not documents:
            raise HTTPException(status_code=400, detail="No text extracted from PDF.")

        document_id = os.path.basename(tmp_path)
        DOCUMENT_STORE[document_id] = documents

        return {
            "document_id": document_id,
            "num_chunks": len(documents),
        }

    finally:
        os.remove(tmp_path)


# -------------------------
# RAG Question Endpoint
# -------------------------
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    if request.document_id not in DOCUMENT_STORE:
        raise HTTPException(status_code=404, detail="Document not found.")

    documents = DOCUMENT_STORE[request.document_id]

    chain = build_rag_chain(
        documents=documents,
        k=request.k,
        fetch_k=request.fetch_k,
    )

    answer = chain.invoke(request.question)

    return AnswerResponse(answer=answer)