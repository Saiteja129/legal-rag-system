"""
PostgreSQL / pgvector connection management and schema setup.

Uses psycopg2 connection pooling for efficient DB access.
Schema includes:
  - documents table with VECTOR(1536) column for embeddings
  - TSVECTOR column for native PostgreSQL full-text search (BM25 proxy)
  - HNSW index on embeddings, GIN index on tsvector
"""

import logging
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool, extras

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)

# ── Connection Pool ───────────────────────────────────────────────────────────

_pool: pool.ThreadedConnectionPool | None = None


def get_pool() -> pool.ThreadedConnectionPool:
    """Lazily initialize and return the connection pool."""
    global _pool
    if _pool is None or _pool.closed:
        if not config.DB_URL:
            raise RuntimeError(
                "DB_URL not configured. Set it in .env (local) or "
                "Hugging Face Space Secrets (production)."
            )
        _pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=5,
            dsn=config.DB_URL,
        )
        logger.info("PostgreSQL connection pool created.")
    return _pool


@contextmanager
def get_connection():
    """Context manager that checks out a connection and returns it on exit."""
    p = get_pool()
    conn = p.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        p.putconn(conn)


# ── Schema Setup ──────────────────────────────────────────────────────────────

SCHEMA_SQL = """
-- Enable pgvector extension (must be done by superuser / already enabled on Neon)
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
    id          SERIAL PRIMARY KEY,
    content     TEXT NOT NULL,
    embedding   VECTOR(1536),
    metadata    JSONB DEFAULT '{}'::jsonb,
    ts_content  TSVECTOR,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-generate tsvector on insert/update
CREATE OR REPLACE FUNCTION documents_ts_trigger() RETURNS trigger AS $$
BEGIN
    NEW.ts_content := to_tsvector('english', NEW.content);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_documents_ts ON documents;
CREATE TRIGGER trg_documents_ts
    BEFORE INSERT OR UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION documents_ts_trigger();

-- HNSW index for fast approximate nearest-neighbor vector search
CREATE INDEX IF NOT EXISTS idx_documents_embedding_hnsw
    ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- GIN index for fast full-text search
CREATE INDEX IF NOT EXISTS idx_documents_ts_content
    ON documents USING gin (ts_content);

-- JSONB index for metadata queries
CREATE INDEX IF NOT EXISTS idx_documents_metadata
    ON documents USING gin (metadata);
"""


def ensure_schema() -> None:
    """Create tables, indexes, and triggers if they don't exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
    logger.info("Database schema verified / created.")


def get_document_count() -> int:
    """Return total number of indexed document chunks."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM documents;")
            return cur.fetchone()[0]


def clear_documents() -> None:
    """Delete all documents (useful for re-indexing)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE documents RESTART IDENTITY;")
    logger.info("All documents cleared.")
