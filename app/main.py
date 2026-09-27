from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Enterprise RAG Pipeline",
    description="Production-oriented RAG API for enterprise knowledge retrieval.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG Pipeline API",
        "version": "1.0.0",
        "docs": "/docs",
    }