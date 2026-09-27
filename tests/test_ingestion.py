from app.ingestion.loaders import discover_documents, load_documents


def test_discover_documents():
    documents = discover_documents("data/raw")

    assert len(documents) > 0
    assert all(document.is_file() for document in documents)


def test_load_documents():
    documents = load_documents("data/raw")

    assert len(documents) > 0

    for document in documents:
        assert "file_name" in document
        assert "file_path" in document
        assert "content" in document
        assert document["content"].strip()