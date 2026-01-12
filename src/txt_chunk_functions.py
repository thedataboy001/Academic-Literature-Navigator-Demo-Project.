from __future__ import annotations

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.parse_functions import process_pdf_to_text

def text_to_chunks(
    file_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """
    Read a PDF, convert to text, split into chunks, and return LangChain Documents.
    """
    text = process_pdf_to_text(file_path)
    if not text or not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunk_texts = splitter.split_text(text)

    documents: List[Document] = []
    for i, chunk in enumerate(chunk_texts):
        chunk = chunk.strip()
        if not chunk:
            continue

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "source": file_path,
                    "chunk_index": i,
                    "chunk_chars": len(chunk),
                },
            )
        )

    return documents
