import html
import json
import os
import textwrap
from pathlib import Path

import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv(
    "RAG_API_URL",
    "http://localhost:8000",
)


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render_html(content: str):
    """
    Render custom HTML safely using Streamlit's HTML renderer.
    textwrap.dedent prevents indentation from being interpreted
    as a Markdown code block.
    """
    st.html(
        textwrap.dedent(content).strip()
    )


# ============================================================
# CUSTOM CSS
# ============================================================

render_html(
    """
    <style>

    /* ========================================================
       STREAMLIT HEADER / TOOLBAR
       ======================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }


    /* ========================================================
       GLOBAL APP
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 80% 10%,
                rgba(93, 70, 220, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 20% 80%,
                rgba(0, 170, 255, 0.06),
                transparent 25%
            ),
            #03060d !important;

        color: #f5f7ff !important;
    }

    .stAppViewContainer {
        padding-top: 0 !important;
    }

    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1500px !important;
    }

    html,
    body {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #050914 0%,
                #02050b 100%
            ) !important;

        border-right:
            1px solid rgba(255, 255, 255, 0.06);
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1.2rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 2.5rem;
    }

    .brand-icon {
        width: 62px;
        height: 62px;
        border-radius: 18px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 28px;
        font-weight: 800;
        color: white;

        background:
            linear-gradient(
                135deg,
                #00d9ff 0%,
                #6955ff 50%,
                #8b3dff 100%
            );

        box-shadow:
            0 12px 30px rgba(83, 73, 255, 0.30);
    }

    .brand-title {
        font-size: 18px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 3px;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #63769a;
    }

    .sidebar-section-title {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #7184a8;
        margin: 1.6rem 0 0.8rem;
    }


    /* ========================================================
       SIDEBAR NAVIGATION
       ======================================================== */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 8px;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {
        background:
            rgba(11, 21, 38, 0.75);

        border:
            1px solid rgba(255, 255, 255, 0.05);

        border-radius: 14px;
        padding: 11px 14px;

        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {
        border-color:
            rgba(115, 88, 255, 0.45);

        background:
            rgba(30, 30, 70, 0.75);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label p {
        color: #9eafd0 !important;
        font-weight: 700;
    }


    /* ========================================================
       KNOWLEDGE CARD
       ======================================================== */

    .knowledge-card {
        margin-top: 1rem;
        padding: 20px;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(14, 30, 52, 0.95),
                rgba(7, 17, 32, 0.95)
            );

        border:
            1px solid rgba(91, 128, 181, 0.18);
    }

    .knowledge-number {
        font-size: 28px;
        font-weight: 800;
        color: white;
        margin: 8px 0 2px;
    }

    .knowledge-label {
        font-size: 12px;
        color: #7185aa;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        padding: 15px 0 10px;
    }

    .hero-title {
        font-size: clamp(42px, 5vw, 72px);
        line-height: 0.98;
        font-weight: 900;
        letter-spacing: -3px;
        color: #ffffff;
        margin: 0;
    }

    .hero-gradient {
        background:
            linear-gradient(
                90deg,
                #ffffff 0%,
                #8d6bff 50%,
                #27c7ff 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        margin-top: 22px;
        max-width: 850px;
        font-size: 16px;
        line-height: 1.7;
        color: #7185aa;
    }


    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {
        min-height: 165px;
        padding: 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(13, 27, 48, 0.96),
                rgba(5, 13, 26, 0.96)
            );

        border:
            1px solid rgba(112, 144, 196, 0.16);

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.20);
    }

    .feature-icon {
        width: 42px;
        height: 42px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background:
            rgba(76, 72, 196, 0.25);

        color: #a996ff;

        font-size: 20px;
        margin-bottom: 18px;
    }

    .feature-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #64799e;
        font-size: 12px;
        line-height: 1.6;
    }


    /* ========================================================
       SECTION HEADER
       ======================================================== */

    .section-header {
        padding: 17px 22px;

        border-radius: 16px 16px 0 0;

        background:
            linear-gradient(
                90deg,
                rgba(47, 35, 122, 0.38),
                rgba(8, 26, 40, 0.65)
            );

        border:
            1px solid rgba(112, 88, 255, 0.45);

        border-bottom: none;
    }

    .section-label {
        color: #9cb2d8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    textarea,
    input {
        background: #07101f !important;
        color: #eaf0ff !important;

        border:
            1px solid rgba(113, 143, 190, 0.35) !important;

        border-radius: 12px !important;
    }

    textarea:focus,
    input:focus {
        border-color: #7562ff !important;

        box-shadow:
            0 0 0 1px rgba(117, 98, 255, 0.35) !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #2b3a54 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 12px !important;

        border:
            1px solid rgba(120, 97, 255, 0.55) !important;

        background:
            linear-gradient(
                135deg,
                #4f3abf,
                #6b4cff
            ) !important;

        color: white !important;

        font-weight: 800 !important;
        min-height: 44px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 10px 30px rgba(99, 72, 255, 0.28);
    }


    /* ========================================================
       METRICS
       ======================================================== */

    .metric-card {
        padding: 20px;

        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                rgba(12, 25, 44, 0.96),
                rgba(5, 13, 25, 0.96)
            );

        border:
            1px solid rgba(113, 145, 193, 0.14);
    }

    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #65799d;
        font-weight: 800;
    }

    .metric-value {
        margin-top: 8px;
        font-size: 30px;
        font-weight: 900;
        color: white;
    }


    /* ========================================================
       ANSWER CARD
       ======================================================== */

    .answer-card {
        padding: 25px;
        margin-top: 20px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(12, 26, 45, 0.98),
                rgba(5, 13, 25, 0.98)
            );

        border:
            1px solid rgba(114, 89, 255, 0.35);

        box-shadow:
            0 20px 45px rgba(0, 0, 0, 0.20);
    }

    .answer-title {
        color: #a99aff;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .answer-text {
        color: #dce6fa;
        font-size: 15px;
        line-height: 1.8;
    }


    /* ========================================================
       SOURCE CARDS
       ======================================================== */

    .source-card {
        padding: 18px;
        margin: 10px 0;

        border-radius: 15px;

        background:
            rgba(7, 18, 34, 0.95);

        border:
            1px solid rgba(93, 125, 177, 0.18);
    }

    .source-file {
        color: #ffffff;
        font-weight: 800;
        font-size: 13px;
    }

    .source-meta {
        color: #6e83a8;
        font-size: 11px;
        margin-top: 6px;
    }

    .source-content {
        color: #9eb0cf;
        font-size: 12px;
        line-height: 1.6;
        margin-top: 10px;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 7px;

        padding: 7px 12px;

        border-radius: 20px;

        background:
            rgba(30, 180, 120, 0.10);

        border:
            1px solid rgba(30, 180, 120, 0.22);

        color: #58dca8;

        font-size: 11px;
        font-weight: 800;
    }

    .status-offline {
        display: inline-flex;
        align-items: center;
        gap: 7px;

        padding: 7px 12px;

        border-radius: 20px;

        background:
            rgba(230, 75, 95, 0.10);

        border:
            1px solid rgba(230, 75, 95, 0.22);

        color: #ff7e90;

        font-size: 11px;
        font-weight: 800;
    }


    /* ========================================================
       DOCUMENT CARDS
       ======================================================== */

    .document-card {
        padding: 20px;
        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                rgba(11, 24, 42, 0.96),
                rgba(5, 13, 25, 0.96)
            );

        border:
            1px solid rgba(110, 141, 190, 0.15);

        margin-bottom: 12px;
    }

    .document-name {
        color: white;
        font-weight: 800;
        font-size: 14px;
    }

    .document-type {
        color: #6d81a5;
        font-size: 11px;
        margin-top: 6px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        margin-top: 60px;
        padding-top: 20px;

        border-top:
            1px solid rgba(255, 255, 255, 0.06);

        text-align: center;

        color: #435572;
        font-size: 11px;
    }

    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def check_api() -> bool:
    """Check whether FastAPI is available."""

    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=3,
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def ask_rag(
    question: str,
    top_k: int = 5,
):
    """Send question to the FastAPI RAG endpoint."""

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "question": question,
            "top_k": top_k,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def get_documents():
    """Return enterprise documents from data/raw."""

    raw_dir = Path("data/raw")

    if not raw_dir.exists():
        return []

    return sorted(
        [
            file
            for file in raw_dir.iterdir()
            if file.is_file()
            and file.suffix.lower() in {
                ".txt",
                ".md",
            }
        ]
    )


def get_processed_chunks_count():
    """Return number of indexed chunks."""

    chunks_file = Path(
        "data/processed/chunks.json"
    )

    if not chunks_file.exists():
        return 0

    try:

        with chunks_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            chunks = json.load(file)

        return len(chunks)

    except Exception:
        return 0


def render_source_card(
    source,
    index,
):
    """Render one retrieved source."""

    file_name = html.escape(
        str(
            source.get(
                "file_name",
                "Unknown",
            )
        )
    )

    chunk_index = source.get(
        "chunk_index",
        "N/A",
    )

    similarity = source.get(
        "similarity",
        0,
    )

    content = html.escape(
        str(
            source.get(
                "content",
                "",
            )
        )
    )

    if len(content) > 420:
        content = content[:420] + "..."

    try:
        similarity_value = float(similarity)
    except (TypeError, ValueError):
        similarity_value = 0.0

    render_html(
        f"""
        <div class="source-card">

            <div class="source-file">
                {index}. {file_name}
            </div>

            <div class="source-meta">
                Chunk {chunk_index}
                &nbsp; • &nbsp;
                Similarity {similarity_value:.4f}
            </div>

            <div class="source-content">
                {content}
            </div>

        </div>
        """
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">

            <div class="brand-icon">
                ◇
            </div>

            <div>
                <div class="brand-title">
                    Enterprise RAG
                </div>

                <div class="brand-subtitle">
                    Knowledge Assistant
                </div>
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="sidebar-section-title">
            Navigation
        </div>
        """
    )

    navigation_options = [
        "Chat",
        "Documents",
        "Analytics",
        "Settings",
    ]

    page = st.radio(
        "Navigation",
        navigation_options,
        index=navigation_options.index(
            st.session_state.page
        ),
        label_visibility="collapsed",
    )

    st.session_state.page = page

    render_html(
        """
        <div class="sidebar-section-title">
            Knowledge Base
        </div>
        """
    )

    documents = get_documents()
    chunk_count = get_processed_chunks_count()

    render_html(
        f"""
        <div class="knowledge-card">

            <div style="font-size:18px;">
                ◫
            </div>

            <div class="knowledge-number">
                {len(documents)}
            </div>

            <div class="knowledge-label">
                Enterprise Documents
            </div>

            <div style="height:14px;"></div>

            <div class="knowledge-number">
                {chunk_count}
            </div>

            <div class="knowledge-label">
                Indexed Chunks
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="sidebar-section-title">
            API Status
        </div>
        """
    )

    api_online = check_api()

    if api_online:

        render_html(
            """
            <div class="status-online">
                ● API ONLINE
            </div>
            """
        )

    else:

        render_html(
            """
            <div class="status-offline">
                ● API OFFLINE
            </div>
            """
        )


# ============================================================
# CHAT PAGE
# ============================================================

if st.session_state.page == "Chat":

    render_html(
        """
        <div class="hero">

            <div class="hero-title">
                Enterprise
                <span class="hero-gradient">
                    Knowledge
                </span>
                <br>
                Assistant
            </div>

            <div class="hero-description">
                Ask questions about company policies,
                procedures and internal documentation
                using AI-powered semantic retrieval
                with source attribution.
            </div>

        </div>
        """
    )

    st.write("")

    # --------------------------------------------------------
    # FEATURE CARDS
    # --------------------------------------------------------

    feature_columns = st.columns(4)

    features = [
        (
            "✦",
            "AI-Powered Search",
            "Find relevant enterprise knowledge.",
        ),
        (
            "▣",
            "Source Attribution",
            "Citations with similarity scores.",
        ),
        (
            "◇",
            "Secure & Private",
            "Keep enterprise knowledge controlled.",
        ),
        (
            "⬡",
            "Enterprise Ready",
            "Production-oriented RAG architecture.",
        ),
    ]

    for column, feature in zip(
        feature_columns,
        features,
    ):

        icon, title, description = feature

        with column:

            render_html(
                f"""
                <div class="feature-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-description">
                        {description}
                    </div>

                </div>
                """
            )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # QUERY SECTION
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-header">

            <div class="section-label">
                Ask Your Knowledge Base
            </div>

        </div>
        """
    )

    question = st.text_area(
        "Question",
        placeholder=(
            "Example: How many days can employees "
            "work remotely?"
        ),
        height=120,
        label_visibility="collapsed",
        key="question_input",
    )

    query_col1, query_col2 = st.columns(
        [5, 1],
        vertical_alignment="center",
    )

    with query_col2:

        top_k = st.number_input(
            "Sources",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
        )

    ask_col1, ask_col2 = st.columns(
        [1, 5]
    )

    with ask_col1:

        ask_clicked = st.button(
            "Ask AI",
            use_container_width=True,
        )

    if ask_clicked:

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching the enterprise knowledge base..."
            ):

                try:

                    result = ask_rag(
                        question.strip(),
                        int(top_k),
                    )

                    st.session_state.last_result = result

                    st.session_state.messages.append(
                        {
                            "question": question.strip(),
                            "result": result,
                        }
                    )

                except requests.RequestException:

                    st.error(
                        "Unable to connect to the RAG API."
                    )

                    st.caption(
                        f"API endpoint: {API_URL}"
                    )

                except Exception as exc:

                    st.error(
                        f"An error occurred: {exc}"
                    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    result = st.session_state.last_result

    if result:

        answer = result.get(
            "answer",
            "No answer returned.",
        )

        sources = result.get(
            "sources",
            [],
        )

        answer_html = html.escape(
            str(answer)
        ).replace(
            "\n",
            "<br>",
        )

        render_html(
            f"""
            <div class="answer-card">

                <div class="answer-title">
                    AI Answer
                </div>

                <div class="answer-text">
                    {answer_html}
                </div>

            </div>
            """
        )

        st.write("")

        left, right = st.columns(
            [2, 1]
        )

        with left:

            render_html(
                """
                <div class="section-header">

                    <div class="section-label">
                        Retrieved Sources
                    </div>

                </div>
                """
            )

            if sources:

                for index, source in enumerate(
                    sources,
                    start=1,
                ):

                    render_source_card(
                        source,
                        index,
                    )

            else:

                st.info(
                    "No sources were returned."
                )

        with right:

            render_html(
                """
                <div class="section-header">

                    <div class="section-label">
                        Retrieval Summary
                    </div>

                </div>
                """
            )

            render_html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Sources Retrieved
                    </div>

                    <div class="metric-value">
                        {len(sources)}
                    </div>

                </div>
                """
            )

            st.write("")

            render_html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Top K
                    </div>

                    <div class="metric-value">
                        {int(top_k)}
                    </div>

                </div>
                """
            )


# ============================================================
# DOCUMENTS PAGE
# ============================================================

elif st.session_state.page == "Documents":

    render_html(
        """
        <div class="hero">

            <div class="hero-title">
                Knowledge
                <span class="hero-gradient">
                    Documents
                </span>
            </div>

            <div class="hero-description">
                Enterprise documents currently available
                in the RAG knowledge base.
            </div>

        </div>
        """
    )

    documents = get_documents()

    col1, col2, col3 = st.columns(3)

    with col1:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Documents
                </div>

                <div class="metric-value">
                    {len(documents)}
                </div>

            </div>
            """
        )

    with col2:

        render_html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Indexed Chunks
                </div>

                <div class="metric-value">
                    {chunk_count}
                </div>

            </div>
            """
        )

    with col3:

        render_html(
            """
            <div class="metric-card">

                <div class="metric-label">
                    Format
                </div>

                <div class="metric-value">
                    TXT
                </div>

            </div>
            """
        )

    st.write("")
    st.write("")

    if not documents:

        st.info(
            "No documents found in data/raw."
        )

    else:

        for document in documents:

            try:
                size_kb = (
                    document.stat().st_size
                    / 1024
                )
            except Exception:
                size_kb = 0

            document_name = html.escape(
                document.name
            )

            document_type = (
                document.suffix
                .upper()
                .replace(".", "")
            )

            render_html(
                f"""
                <div class="document-card">

                    <div class="document-name">
                        ◫ &nbsp;
                        {document_name}
                    </div>

                    <div class="document-type">
                        {document_type}
                        &nbsp; • &nbsp;
                        {size_kb:.1f} KB
                    </div>

                </div>
                """
            )


# ============================================================
# ANALYTICS PAGE
# ============================================================

elif st.session_state.page == "Analytics":

    render_html(
        """
        <div class="hero">

            <div class="hero-title">
                Pipeline
                <span class="hero-gradient">
                    Analytics
                </span>
            </div>

            <div class="hero-description">
                Overview of the indexed enterprise
                knowledge pipeline and retrieval system.
            </div>

        </div>
        """
    )

    documents = get_documents()
    chunks = get_processed_chunks_count()

    metric_columns = st.columns(4)

    analytics = [
        (
            "Documents",
            str(len(documents)),
        ),
        (
            "Chunks",
            str(chunks),
        ),
        (
            "Embedding",
            "384D",
        ),
        (
            "Vector DB",
            "pgvector",
        ),
    ]

    for column, (label, value) in zip(
        metric_columns,
        analytics,
    ):

        with column:

            render_html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        {label}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>

                </div>
                """
            )

    st.write("")
    st.write("")

    render_html(
        """
        <div class="section-header">

            <div class="section-label">
                Pipeline Architecture
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="answer-card">

            <div class="answer-text">

                Documents
                &nbsp; → &nbsp;
                Ingestion
                &nbsp; → &nbsp;
                Validation
                &nbsp; → &nbsp;
                Chunking
                &nbsp; → &nbsp;
                Embeddings
                &nbsp; → &nbsp;
                PostgreSQL + pgvector
                &nbsp; → &nbsp;
                Semantic Retrieval
                &nbsp; → &nbsp;
                Groq LLM
                &nbsp; → &nbsp;
                Answer + Sources

            </div>

        </div>
        """
    )


# ============================================================
# SETTINGS PAGE
# ============================================================

elif st.session_state.page == "Settings":

    render_html(
        """
        <div class="hero">

            <div class="hero-title">
                System
                <span class="hero-gradient">
                    Settings
                </span>
            </div>

            <div class="hero-description">
                Configuration and runtime information
                for the Enterprise RAG application.
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="section-header">

            <div class="section-label">
                API Configuration
            </div>

        </div>
        """
    )

    safe_api_url = html.escape(
        API_URL
    )

    render_html(
        f"""
        <div class="answer-card">

            <div class="metric-label">
                RAG API Endpoint
            </div>

            <div class="answer-text">
                {safe_api_url}
            </div>

        </div>
        """
    )

    st.write("")

    api_online = check_api()

    if api_online:

        st.success(
            "FastAPI backend is connected."
        )

    else:

        st.warning(
            "FastAPI backend is not currently reachable."
        )

    render_html(
        """
        <div class="section-header">

            <div class="section-label">
                Technology Stack
            </div>

        </div>
        """
    )

    technologies = [
        "Python",
        "FastAPI",
        "Streamlit",
        "LangChain",
        "Sentence Transformers",
        "PostgreSQL",
        "pgvector",
        "Groq",
        "PySpark",
        "Docker",
    ]

    st.write("")

    for technology in technologies:

        render_html(
            f"""
            <div class="document-card">

                <div class="document-name">
                    ◇ &nbsp;
                    {technology}
                </div>

            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        Enterprise RAG Pipeline
        &nbsp; • &nbsp;
        Retrieval-Augmented Generation
        &nbsp; • &nbsp;
        FastAPI + PostgreSQL + pgvector + Groq

    </div>
    """
)