from app.retrieval.vector_store import VectorStore


def test_vector_store_search():
    vector_store = VectorStore()

    results = vector_store.search(
        query="How many days can employees work remotely?",
        top_k=3,
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 3


def test_search_result_structure():
    vector_store = VectorStore()

    results = vector_store.search(
        query="What is the annual leave allowance?",
        top_k=3,
    )

    assert len(results) > 0

    result = results[0]

    assert "chunk_id" in result
    assert "document_id" in result
    assert "file_name" in result
    assert "chunk_index" in result
    assert "content" in result
    assert "similarity" in result


def test_similarity_score():
    vector_store = VectorStore()

    results = vector_store.search(
        query="What expenses can employees claim?",
        top_k=3,
    )

    assert len(results) > 0

    for result in results:
        assert isinstance(result["similarity"], float)
        assert -1.0 <= result["similarity"] <= 1.0