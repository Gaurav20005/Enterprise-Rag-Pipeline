\# Enterprise RAG Pipeline — Architecture



```mermaid

flowchart TD



&#x20;   %% =========================

&#x20;   %% INGESTION PIPELINE

&#x20;   %% =========================



&#x20;   A\[Enterprise Documents<br/>TXT / Markdown]



&#x20;   A --> B\[Document Ingestion]



&#x20;   B --> C\[Validation \& Cleaning]



&#x20;   C --> D\[Recursive Text Chunking<br/>500 chars / 50 overlap]



&#x20;   D --> E\[Embedding Generation<br/>all-MiniLM-L6-v2<br/>384 Dimensions]



&#x20;   E --> F\[(PostgreSQL + pgvector<br/>Vector Database)]





&#x20;   %% =========================

&#x20;   %% SERVING PIPELINE

&#x20;   %% =========================



&#x20;   U\[User]



&#x20;   U --> UI\[Streamlit UI]



&#x20;   UI --> API\[FastAPI<br/>/search \& /ask]



&#x20;   API --> RAG\[RAG Service]



&#x20;   RAG --> QE\[Query Embedding<br/>Sentence Transformers]



&#x20;   QE --> F



&#x20;   F --> S\[Semantic Search<br/>Top-K Relevant Chunks]



&#x20;   S --> CTX\[Context Assembly]



&#x20;   CTX --> LLM\[Groq LLM<br/>Grounded Generation]



&#x20;   LLM --> ANS\[Answer + Sources]



&#x20;   ANS --> API



&#x20;   API --> UI





&#x20;   %% =========================

&#x20;   %% BATCH PROCESSING

&#x20;   %% =========================



&#x20;   D --> PS\[PySpark<br/>Batch Processing]



&#x20;   PS --> STATS\[spark\_chunk\_statistics.json]





&#x20;   %% =========================

&#x20;   %% STYLING

&#x20;   %% =========================



&#x20;   classDef ingestion fill:#e8f1ff,stroke:#2563eb,stroke-width:1.5px;

&#x20;   classDef storage fill:#e8f5e9,stroke:#16a34a,stroke-width:1.5px;

&#x20;   classDef serving fill:#fff7ed,stroke:#ea580c,stroke-width:1.5px;

&#x20;   classDef ui fill:#f5f3ff,stroke:#7c3aed,stroke-width:1.5px;

&#x20;   classDef batch fill:#fdf2f8,stroke:#db2777,stroke-width:1.5px;



&#x20;   class A,B,C,D,E ingestion;

&#x20;   class F storage;

&#x20;   class U,UI,API,RAG,QE,S,CTX,LLM,ANS serving;

&#x20;   class UI,U ui;

&#x20;   class PS,STATS batch;

