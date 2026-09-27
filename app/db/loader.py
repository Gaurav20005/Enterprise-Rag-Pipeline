import json
import os
from pathlib import Path

import psycopg2
from pgvector.psycopg2 import register_vector


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "rag_db"),
    "user": os.getenv("DB_USER", "rag_user"),
    "password": os.getenv("DB_PASSWORD", "rag_password"),
}

DOCUMENTS_FILE = "data/processed/documents.json"
EMBEDDED_CHUNKS_FILE = "data/processed/embedded_chunks.json"


def get_connection():
    connection = psycopg2.connect(**DB_CONFIG)
    register_vector(connection)
    return connection


def load_json(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def insert_documents(connection, documents: list[dict]) -> int:
    query = """
        INSERT INTO documents (
            document_id,
            file_name,
            file_path,
            file_extension,
            file_size_bytes,
            ingested_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (document_id)
        DO UPDATE SET
            file_name = EXCLUDED.file_name,
            file_path = EXCLUDED.file_path,
            file_extension = EXCLUDED.file_extension,
            file_size_bytes = EXCLUDED.file_size_bytes,
            ingested_at = EXCLUDED.ingested_at;
    """

    inserted_count = 0

    with connection.cursor() as cursor:
        for document in documents:
            cursor.execute(
                query,
                (
                    document["document_id"],
                    document["file_name"],
                    document["file_path"],
                    document["file_extension"],
                    document["file_size_bytes"],
                    document["ingested_at"],
                ),
            )

            inserted_count += 1

    connection.commit()

    return inserted_count


def insert_chunks(connection, chunks: list[dict]) -> int:
    query = """
        INSERT INTO document_chunks (
            chunk_id,
            document_id,
            file_name,
            chunk_index,
            chunk_size,
            content,
            embedding
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (chunk_id)
        DO UPDATE SET
            document_id = EXCLUDED.document_id,
            file_name = EXCLUDED.file_name,
            chunk_index = EXCLUDED.chunk_index,
            chunk_size = EXCLUDED.chunk_size,
            content = EXCLUDED.content,
            embedding = EXCLUDED.embedding;
    """

    inserted_count = 0

    with connection.cursor() as cursor:
        for chunk in chunks:
            cursor.execute(
                query,
                (
                    chunk["chunk_id"],
                    chunk["document_id"],
                    chunk["file_name"],
                    chunk["chunk_index"],
                    chunk["chunk_size"],
                    chunk["content"],
                    chunk["embedding"],
                ),
            )

            inserted_count += 1

    connection.commit()

    return inserted_count


def main():
    print("Starting PostgreSQL data loading...")

    documents = load_json(DOCUMENTS_FILE)
    chunks = load_json(EMBEDDED_CHUNKS_FILE)

    print(f"Loaded {len(documents)} documents.")
    print(f"Loaded {len(chunks)} chunks.")

    connection = None

    try:
        connection = get_connection()

        document_count = insert_documents(
            connection,
            documents,
        )

        print(f"Documents loaded: {document_count}")

        chunk_count = insert_chunks(
            connection,
            chunks,
        )

        print(f"Chunks loaded: {chunk_count}")

        print()
        print("PostgreSQL loading completed successfully.")

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    main()