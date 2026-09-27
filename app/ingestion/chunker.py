import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


INPUT_FILE = "data/processed/documents.json"
OUTPUT_FILE = "data/processed/chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents(input_file: str) -> list[dict]:
    """
    Load processed documents from JSON.
    """

    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Create the recursive text splitter used
    to divide documents into retrieval-friendly chunks.
    """

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def generate_chunks(
    documents: list[dict],
) -> list[dict]:
    """
    Split documents into overlapping chunks
    while preserving document metadata.
    """

    splitter = create_text_splitter()

    chunks = []

    for document in documents:

        document_id = document["document_id"]
        file_name = document["file_name"]
        content = document["content"]

        document_chunks = splitter.split_text(
            content
        )

        for chunk_index, chunk_content in enumerate(
            document_chunks
        ):

            chunk_id = (
                f"{document_id[:16]}_"
                f"{chunk_index:04d}"
            )

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": document_id,
                    "file_name": file_name,
                    "chunk_index": chunk_index,
                    "chunk_size": len(chunk_content),
                    "content": chunk_content,
                }
            )

    return chunks


def save_chunks(
    chunks: list[dict],
    output_file: str,
) -> None:
    """
    Save generated chunks to JSON.
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

    print("Starting document chunking...")

    documents = load_documents(
        INPUT_FILE
    )

    print(
        f"Loaded {len(documents)} documents."
    )

    chunks = generate_chunks(
        documents
    )

    save_chunks(
        chunks,
        OUTPUT_FILE,
    )

    print(
        f"Generated {len(chunks)} chunks."
    )

    print(
        f"Output written to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()