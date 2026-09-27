import os

import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector

from app.services.embeddings import EmbeddingService


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "rag_db"),
    "user": os.getenv("DB_USER", "rag_user"),
    "password": os.getenv("DB_PASSWORD", "rag_password"),
}


class VectorStore:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def get_connection(self):
        connection = psycopg2.connect(**DB_CONFIG)
        register_vector(connection)
        return connection

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query_embedding = np.array(
            self.embedding_service.generate_embedding(query),
            dtype=np.float32,
        )

        connection = None

        try:
            connection = self.get_connection()

            sql = """
                SELECT
                    chunk_id,
                    document_id,
                    file_name,
                    chunk_index,
                    content,
                    1 - (embedding <=> %s) AS similarity
                FROM document_chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s;
            """

            with connection.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        query_embedding,
                        query_embedding,
                        top_k,
                    ),
                )

                rows = cursor.fetchall()

            results = []

            for row in rows:
                results.append(
                    {
                        "chunk_id": row[0],
                        "document_id": row[1],
                        "file_name": row[2],
                        "chunk_index": row[3],
                        "content": row[4],
                        "similarity": float(row[5]),
                    }
                )

            return results

        finally:
            if connection:
                connection.close()


def main():
    print("Initializing semantic retrieval...")

    vector_store = VectorStore()

    query = input(
        "\nEnter your question: "
    ).strip()

    results = vector_store.search(
        query=query,
        top_k=5,
    )

    print()
    print("=" * 70)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 70)

    for index, result in enumerate(
        results,
        start=1,
    ):
        print()
        print(f"Result {index}")
        print("-" * 70)

        print(
            f"File: {result['file_name']}"
        )

        print(
            f"Chunk: {result['chunk_index']}"
        )

        print(
            f"Similarity: {result['similarity']:.4f}"
        )

        print()
        print(result["content"])

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()