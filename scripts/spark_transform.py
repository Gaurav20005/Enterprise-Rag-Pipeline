import json
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, count, avg, min, max


INPUT_FILE = "data/processed/chunks.json"
OUTPUT_FILE = "data/processed/spark_chunk_statistics.json"


def create_spark_session():
    return (
        SparkSession.builder
        .appName("EnterpriseRAGChunkProcessing")
        .master("local[*]")
        .getOrCreate()
    )


def load_chunks(input_file: str) -> list[dict]:
    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("Starting PySpark batch processing...")

    spark = create_spark_session()

    try:
        chunks = load_chunks(INPUT_FILE)

        print()
        print(f"Loaded chunks from JSON: {len(chunks)}")

        # Convert Python records into a Spark DataFrame.
        df = spark.createDataFrame(chunks)

        print()
        print("Input schema:")
        df.printSchema()

        print()
        print(f"Total chunks: {df.count()}")

        # Calculate content length for every chunk.
        enriched_df = df.withColumn(
            "content_length",
            length(col("content"))
        )

        # Calculate batch-level statistics.
        statistics_df = enriched_df.agg(
            count("*").alias("total_chunks"),
            avg("content_length").alias("average_chunk_length"),
            min("content_length").alias("minimum_chunk_length"),
            max("content_length").alias("maximum_chunk_length"),
        )

        print()
        print("Chunk statistics:")
        statistics_df.show(truncate=False)

        # Convert statistics to JSON.
        statistics = [
            row.asDict()
            for row in statistics_df.collect()
        ]

        output_path = Path(OUTPUT_FILE)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with output_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                statistics,
                file,
                indent=2
            )

        print()
        print(
            f"Statistics written to: {OUTPUT_FILE}"
        )

    finally:
        spark.stop()
        print("Spark session stopped.")


if __name__ == "__main__":
    main()