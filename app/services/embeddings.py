from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    """
    Generates vector embeddings for text using
    a Sentence Transformer model.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
    ):
        print(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

        print("Embedding model loaded successfully.")

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return embeddings.tolist()