import json
from pathlib import Path

from app.services.embeddings import EmbeddingService


INPUT_FILE = "data/processed/chunks.json"
OUTPUT_FILE = "data/processed/embedded_chunks.json"


def load_chunks(
    input_file: str,
) -> list[dict]:
    """
    Load chunks from JSON.
    """

    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {input_file}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def save_embeddings(
    chunks: list[dict],
    output_file: str,
) -> None:
    """
    Save chunks with their embeddings.
    """

    path = Path(output_file)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False,
        )


def main():

    print("Starting embedding generation...")

    chunks = load_chunks(
        INPUT_FILE
    )

    print(
        f"Loaded {len(chunks)} chunks."
    )

    embedding_service = EmbeddingService()

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = (
        embedding_service.generate_embeddings(
            texts
        )
    )

    if len(embeddings) != len(chunks):
        raise RuntimeError(
            "Number of embeddings does not match "
            "number of chunks."
        )

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):

        chunk["embedding"] = embedding

        chunk["embedding_dimension"] = len(
            embedding
        )

    save_embeddings(
        chunks,
        OUTPUT_FILE,
    )

    print()
    print(
        f"Generated {len(embeddings)} embeddings."
    )

    print(
        f"Embedding dimension: "
        f"{len(embeddings[0])}"
    )

    print(
        f"Output written to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()