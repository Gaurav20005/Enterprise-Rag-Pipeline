from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
}


def discover_documents(source_dir: str) -> list[Path]:
    """
    Discover supported documents from the source directory.
    """

    directory = Path(source_dir)

    if not directory.exists():
        raise FileNotFoundError(
            f"Source directory does not exist: {source_dir}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Source path is not a directory: {source_dir}"
        )

    documents = [
        path
        for path in directory.iterdir()
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    return sorted(documents)


def load_text_document(file_path: Path) -> str:
    """
    Read a text or markdown document using UTF-8 encoding.
    """

    try:
        return file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError as exc:
        raise ValueError(
            f"Unable to decode document as UTF-8: {file_path}"
        ) from exc


def load_documents(source_dir: str) -> list[dict]:
    """
    Discover and load all supported documents.
    """

    documents = []

    for file_path in discover_documents(source_dir):

        content = load_text_document(file_path)

        documents.append(
            {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "file_extension": file_path.suffix.lower(),
                "content": content,
            }
        )

    return documents