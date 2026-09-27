CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    document_id VARCHAR(64) NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_extension VARCHAR(20),
    file_size_bytes BIGINT,
    ingested_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    chunk_id VARCHAR(100) NOT NULL UNIQUE,
    document_id VARCHAR(64) NOT NULL,
    file_name TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_size INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_document
        FOREIGN KEY (document_id)
        REFERENCES documents(document_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id
ON document_chunks(document_id);

CREATE INDEX IF NOT EXISTS idx_document_chunks_file_name
ON document_chunks(file_name);