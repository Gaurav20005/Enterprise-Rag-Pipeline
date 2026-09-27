from app.ingestion.validator import (
    validate_document,
    validate_documents,
)


def test_valid_document():
    document = {
        "document_id": "a" * 64,
        "file_name": "test_policy.txt",
        "file_path": "data/raw/test_policy.txt",
        "file_extension": ".txt",
        "file_size_bytes": 1000,
        "ingested_at": "2026-09-26T00:00:00+00:00",
        "content": "This is a valid enterprise policy document. " * 5,
    }

    errors = validate_document(document)

    assert errors == []


def test_invalid_document():
    document = {
        "document_id": "invalid",
        "file_name": "test_policy.pdf",
        "file_path": "data/raw/test_policy.pdf",
        "file_extension": ".pdf",
        "file_size_bytes": 0,
        "ingested_at": "2026-09-26T00:00:00+00:00",
        "content": "",
    }

    errors = validate_document(document)

    assert len(errors) > 0


def test_validate_documents():
    documents = [
        {
            "document_id": "a" * 64,
            "file_name": "policy1.txt",
            "file_path": "data/raw/policy1.txt",
            "file_extension": ".txt",
            "file_size_bytes": 1000,
            "ingested_at": "2026-09-26T00:00:00+00:00",
            "content": "This is a valid enterprise policy document. " * 5,
        }
    ]

    report = validate_documents(documents)

    assert report["summary"]["total_documents"] == 1
    assert report["summary"]["valid_documents"] == 1
    assert report["summary"]["invalid_documents"] == 0
    assert report["summary"]["pipeline_status"] == "PASS"