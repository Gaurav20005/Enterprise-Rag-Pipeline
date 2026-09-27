import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from app.ingestion.loaders import load_documents


SOURCE_DIRECTORY = "data/raw"
OUTPUT_FILE = "data/processed/documents.json"


def calculate_sha256(content: str) -> str:
    """
    Generate a SHA-256 hash for document content.
    """

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def clean_text(text: str) -> str:
    """
    Perform basic text normalization.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
    ]

    cleaned_lines = [
        line
        for line in lines
        if line
    ]

    return "\n".join(cleaned_lines)


def extract_document_metadata(
    file_name: str,
    file_path: str,
    content: str,
) -> dict:

    path = Path(file_path)

    return {
        "document_id": calculate_sha256(content),
        "file_name": file_name,
        "file_path": file_path,
        "file_extension": path.suffix.lower(),
        "file_size_bytes": path.stat().st_size,
        "ingested_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


def process_documents() -> list[dict]:
    """
    Execute the document ingestion pipeline.
    """

    raw_documents = load_documents(
        SOURCE_DIRECTORY
    )

    processed_documents = []

    seen_hashes = set()

    for document in raw_documents:

        original_content = document["content"]

        cleaned_content = clean_text(
            original_content
        )

        document_hash = calculate_sha256(
            cleaned_content
        )

        if document_hash in seen_hashes:
            print(
                f"Skipping duplicate: "
                f"{document['file_name']}"
            )
            continue

        seen_hashes.add(document_hash)

        metadata = extract_document_metadata(
            file_name=document["file_name"],
            file_path=document["file_path"],
            content=cleaned_content,
        )

        processed_document = {
            **metadata,
            "content": cleaned_content,
        }

        processed_documents.append(
            processed_document
        )

    return processed_documents


def save_documents(
    documents: list[dict],
    output_file: str,
) -> None:

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            documents,
            file,
            indent=2,
            ensure_ascii=False,
        )


def main():

    print("Starting document ingestion...")

    documents = process_documents()

    save_documents(
        documents,
        OUTPUT_FILE,
    )

    print(
        f"Successfully processed "
        f"{len(documents)} documents."
    )

    print(
        f"Output written to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()