from app.ingestion.chunker import (
    create_text_splitter,
    generate_chunks,
)


def test_text_splitter():
    splitter = create_text_splitter()

    text = "This is a test document. " * 100
    chunks = splitter.split_text(text)

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) <= 500


def test_generate_chunks():
    documents = [
        {
            "document_id": "a" * 64,
            "file_name": "test_policy.txt",
            "content": (
                "This is an enterprise policy document. "
                * 100
            ),
        }
    ]

    chunks = generate_chunks(documents)

    assert len(chunks) > 1

    for index, chunk in enumerate(chunks):
        assert chunk["document_id"] == "a" * 64
        assert chunk["file_name"] == "test_policy.txt"
        assert chunk["chunk_index"] == index
        assert chunk["content"]
        assert chunk["chunk_size"] == len(chunk["content"])


def test_chunk_ids_are_unique():
    documents = [
        {
            "document_id": "b" * 64,
            "file_name": "policy.txt",
            "content": "Enterprise policy content. " * 100,
        }
    ]

    chunks = generate_chunks(documents)

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))