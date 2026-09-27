from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.retrieval.vector_store import VectorStore
from app.services.rag_service import RAGService


router = APIRouter()

vector_store = VectorStore()
rag_service = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "enterprise-rag-pipeline",
    }


@router.post("/search")
def search(request: SearchRequest):
    try:
        results = vector_store.search(
            query=request.query,
            top_k=request.top_k,
        )

        return {
            "query": request.query,
            "results": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/ask")
def ask(request: AskRequest):
    global rag_service

    try:
        if rag_service is None:
            rag_service = RAGService()

        result = rag_service.ask(
            question=request.question,
            top_k=request.top_k,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )