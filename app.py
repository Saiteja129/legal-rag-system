"""
Legal RAG System — Streamlit Dashboard
Hosted on Hugging Face Spaces

Features:
  - Left Sidebar: PDF upload, index status, re-index controls
  - Main Area: Professional chat interface with streaming responses
  - Bottom Expander: System health (RAGAS scores) + Source Transparency
"""

import json
import time
import logging
from pathlib import Path

import streamlit as st
import pandas as pd

# ── Page Config (must be first Streamlit command) ─────────────────────────────
st.set_page_config(
    page_title="Legal RAG — UK Financial Compliance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports (after page config) ───────────────────────────────────────────────
import config
from engine.db import ensure_schema, get_document_count
from engine.document_processor import process_pdf
from engine.hybrid_search import hybrid_search, generate_answer

logger = logging.getLogger(__name__)

# ── Results file path ─────────────────────────────────────────────────────────
RESULTS_PATH = Path(__file__).parent / "evaluation" / "results" / "results.json"


# ══════════════════════════════════════════════════════════════════════════════
#  CSS — Premium dark theme with glassmorphism
# ══════════════════════════════════════════════════════════════════════════════

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ────────────────────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header ────────────────────────────────────────── */
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #4c1d95 60%, #7c3aed 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(124, 58, 237, 0.3);
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);
    }
    .main-header h1 {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #c4b5fd;
        font-size: 0.95rem;
        margin: 0.3rem 0 0 0;
        font-weight: 400;
    }

    /* ── Glass Card ────────────────────────────────────── */
    .glass-card {
        background: rgba(30, 27, 75, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(124, 58, 237, 0.5);
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.1);
        transform: translateY(-1px);
    }
    .glass-card .source-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #a78bfa;
        margin-bottom: 0.4rem;
    }
    .glass-card .source-content {
        font-size: 0.85rem;
        color: #e2e8f0;
        line-height: 1.6;
    }
    .glass-card .source-meta {
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        display: flex;
        gap: 1rem;
    }

    /* ── Score Badge ───────────────────────────────────── */
    .score-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .score-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
    .score-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
    .score-red   { background: rgba(239, 68, 68, 0.15); color: #f87171; }

    /* ── Chat Messages ─────────────────────────────────── */
    .chat-user {
        background: linear-gradient(135deg, #312e81, #4c1d95);
        border-radius: 16px 16px 4px 16px;
        padding: 1rem 1.4rem;
        margin: 0.5rem 0;
        color: #f1f5f9;
        max-width: 85%;
        margin-left: auto;
    }
    .chat-assistant {
        background: rgba(30, 27, 75, 0.5);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 16px 16px 16px 4px;
        padding: 1rem 1.4rem;
        margin: 0.5rem 0;
        color: #e2e8f0;
        max-width: 85%;
    }

    /* ── Sidebar Stats ─────────────────────────────────── */
    .stat-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(79, 70, 229, 0.05));
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #a78bfa;
    }
    .stat-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        font-weight: 500;
    }

    /* ── Metric Row ────────────────────────────────────── */
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0;
        border-bottom: 1px solid rgba(124, 58, 237, 0.1);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.82rem;
    }

    /* ── Pulse Animation ───────────────────────────────── */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .pulse { animation: pulse 2s ease-in-out infinite; }

    /* ── Hide Streamlit branding ───────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Helper Functions
# ══════════════════════════════════════════════════════════════════════════════

def score_badge(score: float) -> str:
    """Return HTML badge with color based on score threshold."""
    if score >= 0.85:
        cls = "score-green"
    elif score >= 0.70:
        cls = "score-amber"
    else:
        cls = "score-red"
    return f'<span class="score-badge {cls}">{score:.2f}</span>'


def load_ragas_scores() -> dict | None:
    """Load latest RAGAS evaluation scores."""
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, "r") as f:
            return json.load(f)
    return None


def init_session_state():
    """Initialize Streamlit session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_sources" not in st.session_state:
        st.session_state.last_sources = []
    if "db_initialized" not in st.session_state:
        st.session_state.db_initialized = False


def initialize_db():
    """Initialize database schema if not already done."""
    if not st.session_state.db_initialized:
        try:
            ensure_schema()
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"⚠️ Database connection failed: {str(e)}")
            st.info("Please check your DB_URL in environment secrets.")
            st.session_state.db_initialized = False


# ══════════════════════════════════════════════════════════════════════════════
#  Sidebar
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚖️ Legal RAG Engine")
        st.caption("UK Financial Compliance AI")

        st.divider()

        # ── PDF Upload ────────────────────────────────────────────────────
        st.markdown("#### 📄 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload UK financial compliance documents for indexing",
            key="pdf_uploader",
        )

        if uploaded_files:
            if st.button("🔄 Index Documents", use_container_width=True, type="primary"):
                with st.spinner("Processing documents..."):
                    total_chunks = 0
                    for file in uploaded_files:
                        stats = process_pdf(file, filename=file.name)
                        if "error" not in stats:
                            total_chunks += stats["chunk_count"]
                            st.success(
                                f"✅ {file.name}: {stats['chunk_count']} chunks "
                                f"({stats['total_time_s']}s)"
                            )
                        else:
                            st.error(f"❌ {file.name}: {stats['error']}")
                    if total_chunks > 0:
                        st.balloons()

        st.divider()

        # ── Index Status ──────────────────────────────────────────────────
        st.markdown("#### 📊 Index Status")

        try:
            doc_count = get_document_count() if st.session_state.db_initialized else 0
        except Exception:
            doc_count = 0

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-value">{doc_count:,}</div>'
                f'<div class="stat-label">Chunks Indexed</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col2:
            status = "🟢 Online" if st.session_state.db_initialized else "🔴 Offline"
            st.markdown(
                f'<div class="stat-card">'
                f'<div class="stat-value" style="font-size:1.2rem">{status}</div>'
                f'<div class="stat-label">Database</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Engine Config ─────────────────────────────────────────────────
        st.markdown("#### ⚙️ Engine Config")
        st.caption(f"**Embedding**: {config.EMBEDDING_MODEL}")
        st.caption(f"**LLM**: {config.LLM_MODEL}")
        st.caption(f"**Reranker**: ms-marco-MiniLM-L-6-v2")
        st.caption(f"**Chunk Size**: {config.CHUNK_SIZE} / Overlap: {config.CHUNK_OVERLAP}")
        st.caption(f"**RRF k**: {config.RRF_K}")


# ══════════════════════════════════════════════════════════════════════════════
#  Main Chat Area
# ══════════════════════════════════════════════════════════════════════════════

def render_chat():
    # Header
    st.markdown(
        '<div class="main-header">'
        '<h1>⚖️ Legal RAG — UK Financial Compliance</h1>'
        '<p>Hybrid search engine powered by Vector + BM25 + RRF + Cross-Encoder reranking</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about UK financial regulations...", key="chat_input"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            if not st.session_state.db_initialized:
                response = (
                    "⚠️ Database is not connected. Please configure your `DB_URL` "
                    "in the Hugging Face Space secrets and ensure documents are indexed."
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                return

            with st.spinner("🔍 Searching with hybrid engine..."):
                try:
                    # Run hybrid search
                    search_results = hybrid_search(prompt, top_k=10)
                    st.session_state.last_sources = search_results

                    if not search_results:
                        response = (
                            "I couldn't find any relevant documents for your query. "
                            "Please ensure documents have been uploaded and indexed."
                        )
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        return

                    # Generate answer
                    response = generate_answer(prompt, search_results)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


# ══════════════════════════════════════════════════════════════════════════════
#  Bottom Section — System Health + Source Transparency
# ══════════════════════════════════════════════════════════════════════════════

def render_bottom_section():
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    # ── System Health ─────────────────────────────────────────────────────
    with col1:
        with st.expander("🏥 System Health — RAGAS Scores", expanded=False):
            scores = load_ragas_scores()
            if scores:
                st.markdown(
                    f'<div class="metric-row">'
                    f'<span class="metric-label">Faithfulness</span>'
                    f'{score_badge(scores["faithfulness"])}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="metric-row">'
                    f'<span class="metric-label">Answer Relevancy</span>'
                    f'{score_badge(scores["answer_relevancy"])}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="metric-row">'
                    f'<span class="metric-label">Questions Evaluated</span>'
                    f'<span style="color:#e2e8f0; font-weight:600;">{scores.get("total_questions", "N/A")}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="metric-row">'
                    f'<span class="metric-label">Last Evaluated</span>'
                    f'<span style="color:#94a3b8; font-size:0.8rem;">{scores.get("timestamp", "N/A")}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                status = "✅ Passed" if scores.get("passed") else "❌ Failed"
                st.markdown(
                    f'<div class="metric-row" style="border:none">'
                    f'<span class="metric-label">Quality Gate</span>'
                    f'<span style="font-weight:600;">{status}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.info(
                    "No evaluation results found. Run the RAGAS evaluation pipeline "
                    "to see quality scores here."
                )

    # ── Source Transparency ───────────────────────────────────────────────
    with col2:
        with st.expander("🔎 Source Transparency — Retrieved Chunks", expanded=False):
            sources = st.session_state.get("last_sources", [])
            if sources:
                for i, source in enumerate(sources, 1):
                    metadata = source.get("metadata", {})
                    source_file = metadata.get("source_file", "Unknown")
                    chunk_idx = metadata.get("chunk_index", "?")
                    source_ranks = source.get("source_ranks", {})

                    # Build provenance tags
                    tags = []
                    if "vector_rank" in source_ranks:
                        tags.append(f"Vector: #{source_ranks['vector_rank']}")
                    if "bm25_rank" in source_ranks:
                        tags.append(f"BM25: #{source_ranks['bm25_rank']}")

                    tags_str = " · ".join(tags) if tags else "N/A"

                    content_preview = source["content"][:300]
                    if len(source["content"]) > 300:
                        content_preview += "..."

                    st.markdown(
                        f'<div class="glass-card">'
                        f'<div class="source-label">Source {i} · {source_file} · Chunk {chunk_idx}</div>'
                        f'<div class="source-content">{content_preview}</div>'
                        f'<div class="source-meta">'
                        f'<span>Score: {score_badge(source.get("score", 0))}</span>'
                        f'<span>RRF: {source.get("rrf_score", 0):.4f}</span>'
                        f'<span>{tags_str}</span>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("Ask a question above to see the retrieved source chunks here.")


# ══════════════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    inject_custom_css()
    init_session_state()
    initialize_db()
    render_sidebar()
    render_chat()
    render_bottom_section()


if __name__ == "__main__":
    main()
