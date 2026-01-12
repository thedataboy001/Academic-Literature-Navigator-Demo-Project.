import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

from typing import List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def format_docs(docs: List[Document]) -> str:
    parts = []
    for d in docs:
        pid = d.metadata.get("paper_id") or d.metadata.get("source") or "unknown"
        year = d.metadata.get("year", "unknown")
        page = d.metadata.get("page", d.metadata.get("page_number", "unknown"))
        sec = d.metadata.get("section", "unknown")

        cite = f"[{pid}, {year}, p.{page}, {sec}]"
        parts.append(f"{cite} {d.page_content}")
    return "\n\n".join(parts)


def build_rag_chain(
    documents: List[Document],
    k: int = 8,
    fetch_k: int = 20,
):
    vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": fetch_k},
    )

    rag_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an academic research assistant.\n"
                "Answer ONLY using the provided sources.\n"
                "Cite each claim using [paper_id, year, page, section] as given in the sources.\n"
                "If evidence is insufficient, say so.\n",
            ),
            (
                "human",
                "Question: {question}\n\n"
                "Sources:\n{context}\n\n"
                "Answer:",
            ),
        ]
    )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


