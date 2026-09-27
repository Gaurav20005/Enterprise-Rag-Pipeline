from app.services.embeddings import EmbeddingService


def test_single_embedding():
    service = EmbeddingService()

    embedding = service.generate_embedding(
        "Employees may work remotely up to three days per week."
    )

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert all(isinstance(value, float) for value in embedding)


def test_batch_embeddings():
    service = EmbeddingService()

    texts = [
        "Annual leave policy for employees.",
        "Information security requirements.",
        "Employee expense reimbursement policy.",
    ]

    embeddings = service.generate_embeddings(texts)

    assert len(embeddings) == len(texts)

    for embedding in embeddings:
        assert len(embedding) == 384
        assert all(isinstance(value, float) for value in embedding)