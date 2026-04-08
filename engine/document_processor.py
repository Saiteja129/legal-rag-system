"""
PDF ingestion, text chunking, embedding, and database storage.

Pipeline: PDF → text extraction → recursive chunking → OpenAI embedding → pgvector storage
"""

import logging
import time
from typing import BinaryIO

from PyPDF2 import PdfReader
from openai import OpenAI
from psycopg2 import extras

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from engine.db import get_connection

logger = logging.getLogger(__name__)


# ── PDF Text Extraction ──────────────────────────────────────────────────────

def extract_text_from_pdf(file: BinaryIO, filename: str = "upload.pdf") -> str:
    """Extract all text from a PDF file object."""
    reader = PdfReader(file)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append(f"[Page {i + 1}]\n{text.strip()}")
    full_text = "\n\n".join(pages)
    logger.info(f"Extracted {len(pages)} pages from '{filename}' ({len(full_text)} chars).")
    return full_text


# ── Text Chunking ────────────────────────────────────────────────────────────

def chunk_text(
    text: str,
    chunk_size: int = config.CHUNK_SIZE,
    overlap: int = config.CHUNK_OVERLAP,
) -> list[dict]:
    """
    Split text into overlapping chunks with metadata.
    
    Uses sentence-aware splitting: tries to break on paragraph/sentence
    boundaries rather than mid-word.
    """
    chunks = []
    separators = ["\n\n", "\n", ". ", " "]

    def _split_recursive(text: str, start_idx: int) -> list[dict]:
        if len(text) <= chunk_size:
            if text.strip():
                return [{"content": text.strip(), "char_start": start_idx}]
            return []

        results = []
        pos = 0
        while pos < len(text):
            end = min(pos + chunk_size, len(text))

            # Try to find a natural break point
            if end < len(text):
                best_break = -1
                for sep in separators:
                    # Search backwards from end for separator
                    search_start = max(pos + chunk_size // 2, pos)
                    idx = text.rfind(sep, search_start, end)
                    if idx > best_break:
                        best_break = idx + len(sep)
                if best_break > pos:
                    end = best_break

            chunk_content = text[pos:end].strip()
            if chunk_content:
                results.append({
                    "content": chunk_content,
                    "char_start": start_idx + pos,
                })

            # Move forward with overlap
            pos = end - overlap if end < len(text) else end

        return results

    chunks = _split_recursive(text, 0)

    # Add chunk index
    for i, chunk in enumerate(chunks):
        chunk["chunk_index"] = i

    logger.info(f"Created {len(chunks)} chunks (size={chunk_size}, overlap={overlap}).")
    return chunks


# ── Embedding ─────────────────────────────────────────────────────────────────

def _get_openai_client() -> OpenAI:
    """Return an OpenAI client configured with the API key."""
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured.")
    return OpenAI(api_key=config.OPENAI_API_KEY)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a batch of texts using OpenAI text-embedding-3-small.
    Handles batching internally (max 2048 per API call).
    """
    client = _get_openai_client()
    all_embeddings = []
    batch_size = 512  # safe batch size

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=batch,
            dimensions=config.EMBEDDING_DIMENSIONS,
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


# ── Storage ───────────────────────────────────────────────────────────────────

def store_chunks(
    chunks: list[dict],
    embeddings: list[list[float]],
    source_metadata: dict,
) -> int:
    """
    Store document chunks with embeddings in pgvector.
    
    Args:
        chunks: List of chunk dicts with 'content', 'chunk_index', 'char_start'
        embeddings: Corresponding embedding vectors
        source_metadata: Shared metadata (filename, upload_time, etc.)
    
    Returns:
        Number of chunks stored
    """
    rows = []
    for chunk, emb in zip(chunks, embeddings):
        metadata = {
            **source_metadata,
            "chunk_index": chunk["chunk_index"],
            "char_start": chunk["char_start"],
        }
        rows.append((chunk["content"], emb, extras.Json(metadata)))

    with get_connection() as conn:
        with conn.cursor() as cur:
            extras.execute_values(
                cur,
                """
                INSERT INTO documents (content, embedding, metadata)
                VALUES %s
                """,
                rows,
                template="(%s, %s::vector, %s)",
                page_size=100,
            )

    logger.info(f"Stored {len(rows)} chunks in database.")
    return len(rows)


# ── Full Pipeline ─────────────────────────────────────────────────────────────

def process_pdf(
    file: BinaryIO,
    filename: str = "upload.pdf",
) -> dict:
    """
    End-to-end pipeline: PDF → chunks → embeddings → database.
    
    Returns:
        dict with stats: chunk_count, embedding_time, total_time
    """
    t_start = time.time()

    # Extract text
    text = extract_text_from_pdf(file, filename)
    if not text.strip():
        return {"error": "No text extracted from PDF.", "chunk_count": 0}

    # Chunk
    chunks = chunk_text(text)

    # Embed
    t_embed = time.time()
    texts = [c["content"] for c in chunks]
    embeddings = embed_texts(texts)
    embedding_time = time.time() - t_embed

    # Store
    metadata = {
        "source_file": filename,
        "indexed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    stored = store_chunks(chunks, embeddings, metadata)

    total_time = time.time() - t_start

    stats = {
        "chunk_count": stored,
        "embedding_time_s": round(embedding_time, 2),
        "total_time_s": round(total_time, 2),
        "source_file": filename,
    }
    logger.info(f"Pipeline complete: {stats}")
    return stats
