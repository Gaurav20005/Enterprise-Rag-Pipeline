import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.retrieval.vector_store import VectorStore


load_dotenv()

class RAGService:
    """Retrieval-Augmented Generation service."""

    def __init__(self):
        self.vector_store = VectorStore()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Set it as an environment variable before using RAG generation."
            )

        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
            api_key=api_key,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the supplied context.

Rules:
1. Do not invent information.
2. If the context does not contain enough information, say:
   "I don't have enough information in the provided documents."
3. Keep the answer concise and factual.
4. When useful, mention the source document name.
5. Do not use outside knowledge.

Context:
{context}
""",
                ),
                (
                    "human",
                    "{question}",
                ),
            ]
        )

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """Retrieve relevant context and generate an answer."""

        results = self.vector_store.search(
            query=question,
            top_k=top_k,
        )

        if not results:
            return {
                "question": question,
                "answer": (
                    "I don't have enough information in the "
                    "provided documents."
                ),
                "sources": [],
            }

        context_parts = []

        for result in results:
            context_parts.append(
                f"Source: {result['file_name']}\n"
                f"Content:\n{result['content']}"
            )

        context = "\n\n---\n\n".join(context_parts)

        messages = self.prompt.format_messages(
            context=context,
            question=question,
        )

        response = self.llm.invoke(messages)

        sources = [
            {
                "file_name": result["file_name"],
                "chunk_id": result["chunk_id"],
                "similarity": result["similarity"],
            }
            for result in results
        ]

        return {
            "question": question,
            "answer": response.content,
            "sources": sources,
        }


def main():
    print("Initializing RAG service...")

    rag_service = RAGService()

    question = input("\nEnter your question: ").strip()

    result = rag_service.ask(question)

    print()
    print("=" * 70)
    print("RAG ANSWER")
    print("=" * 70)
    print()
    print(result["answer"])

    print()
    print("=" * 70)
    print("SOURCES")
    print("=" * 70)

    for source in result["sources"]:
        print(
            f"- {source['file_name']} "
            f"(similarity: {source['similarity']:.4f})"
        )


if __name__ == "__main__":
    main()