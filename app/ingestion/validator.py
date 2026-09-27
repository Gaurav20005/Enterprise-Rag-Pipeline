import hashlib
import json
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
}


def validate_document(document: dict) -> list[str]:
    """
    Validate a single document.

    Returns a list of validation errors.
    An empty list means the document passed validation.
    """

    errors = []

    required_fields = [
        "document_id",
        "file_name",
        "file_path",
        "file_extension",
        "file_size_bytes",
        "ingested_at",
        "content",
    ]

    for field in required_fields:
        if field not in document:
            errors.append(
                f"Missing required field: {field}"
            )

    if errors:
        return errors

    content = document["content"]

    if not isinstance(content, str):
        errors.append("Content must be a string.")

    elif not content.strip():
        errors.append("Document content is empty.")

    elif len(content.strip()) < 100:
        errors.append(
            "Document content is shorter than 100 characters."
        )

    extension = document["file_extension"].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        errors.append(
            f"Unsupported file type: {extension}"
        )

    if document["file_size_bytes"] <= 0:
        errors.append(
            "Document file size must be greater than zero."
        )

    document_id = document["document_id"]

    if not isinstance(document_id, str):
        errors.append(
            "Document ID must be a string."
        )

    elif len(document_id) != 64:
        errors.append(
            "Document ID must be a valid SHA-256 hash."
        )

    return errors


def validate_duplicates(documents: list[dict]) -> list[str]:
    """
    Detect duplicate document IDs and filenames.
    """

    errors = []

    document_ids = {}
    filenames = {}

    for document in documents:

        document_id = document.get("document_id")
        filename = document.get("file_name")

        if document_id:
            if document_id in document_ids:
                errors.append(
                    f"Duplicate document ID: {document_id}"
                )
            else:
                document_ids[document_id] = filename

        if filename:
            if filename in filenames:
                errors.append(
                    f"Duplicate filename: {filename}"
                )
            else:
                filenames[filename] = document_id

    return errors


def validate_documents(
    documents: list[dict],
) -> dict:
    """
    Validate the complete document collection.
    """

    document_results = []

    total_errors = []

    for document in documents:

        errors = validate_document(document)

        result = {
            "file_name": document.get(
                "file_name",
                "UNKNOWN",
            ),
            "valid": len(errors) == 0,
            "errors": errors,
        }

        document_results.append(result)

        total_errors.extend(errors)

    duplicate_errors = validate_duplicates(
        documents
    )

    total_errors.extend(duplicate_errors)

    valid_documents = sum(
        1
        for result in document_results
        if result["valid"]
    )

    invalid_documents = (
        len(document_results)
        - valid_documents
    )

    return {
        "summary": {
            "total_documents": len(documents),
            "valid_documents": valid_documents,
            "invalid_documents": invalid_documents,
            "total_errors": len(total_errors),
            "pipeline_status": (
                "PASS"
                if len(total_errors) == 0
                else "FAIL"
            ),
        },
        "documents": document_results,
        "duplicate_errors": duplicate_errors,
    }


def load_processed_documents(
    input_file: str,
) -> list[dict]:

    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Processed document file not found: {input_file}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_validation_report(
    report: dict,
    output_file: str,
) -> None:

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
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )


def main():

    input_file = "data/processed/documents.json"

    output_file = (
        "data/processed/validation_report.json"
    )

    print("Starting data-quality validation...")

    documents = load_processed_documents(
        input_file
    )

    report = validate_documents(
        documents
    )

    save_validation_report(
        report,
        output_file,
    )

    summary = report["summary"]

    print()
    print("Data Quality Report")
    print("-------------------")
    print(
        f"Total documents: "
        f"{summary['total_documents']}"
    )
    print(
        f"Valid documents: "
        f"{summary['valid_documents']}"
    )
    print(
        f"Invalid documents: "
        f"{summary['invalid_documents']}"
    )
    print(
        f"Total errors: "
        f"{summary['total_errors']}"
    )
    print(
        f"Pipeline status: "
        f"{summary['pipeline_status']}"
    )

    print()
    print(
        f"Report written to: {output_file}"
    )


if __name__ == "__main__":
    main()