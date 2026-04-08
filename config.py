"""
Centralized configuration for the Legal RAG System.
Dual-mode secret loading:
  - HF Spaces: reads from st.secrets
  - Local dev: falls back to os.environ / .env file
"""

import os
from dotenv import load_dotenv

# Load .env for local development (no-op if file doesn't exist)
load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """Retrieve a secret from Streamlit secrets (HF Spaces) or environment."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key, default)


# ── Database ──────────────────────────────────────────────────────────────────
DB_URL: str = _get_secret("DB_URL")

# ── OpenAI ────────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = _get_secret("OPENAI_API_KEY")
EMBEDDING_MODEL: str = "text-embedding-3-small"
EMBEDDING_DIMENSIONS: int = 1536
LLM_MODEL: str = "gpt-4o-mini"

# ── Hybrid Search ─────────────────────────────────────────────────────────────
CHUNK_SIZE: int = 512
CHUNK_OVERLAP: int = 64
RRF_K: int = 60                          # Reciprocal Rank Fusion constant
VECTOR_SEARCH_LIMIT: int = 20            # Top-k for vector retrieval
BM25_SEARCH_LIMIT: int = 20              # Top-k for keyword retrieval
RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANKER_TOP_K: int = 10                 # Final results after cross-encoder

# ── Hugging Face ──────────────────────────────────────────────────────────────
HF_TOKEN: str = _get_secret("HF_TOKEN")

# ── Evaluation Thresholds ─────────────────────────────────────────────────────
FAITHFULNESS_THRESHOLD: float = 0.85
RELEVANCY_THRESHOLD: float = 0.85
