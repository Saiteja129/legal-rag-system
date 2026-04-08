"""
Hybrid Search Engine — Vector + BM25 + Reciprocal Rank Fusion + Cross-Encoder Reranking.

Architecture:
  1. Semantic Vector Search  → pgvector cosine distance (top 20)
  2. BM25 Keyword Search     → PostgreSQL tsvector/tsquery (top 20)
  3. Reciprocal Rank Fusion  → Merge both result sets with RRF scoring
  4. Cross-Encoder Reranking → ms-marco-MiniLM-L-6-v2 reranks to final top 10
"""

import logging
from collections import defaultdict

import torch
from sentence_transformers import CrossEncoder
from openai import OpenAI

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from engine.db import get_connection

logger = logging.getLogger(__name__)

# ── Lazy-loaded Models ────────────────────────────────────────────────────────

_cross_encoder: CrossEncoder | None = None
_openai_client: OpenAI | None = None


def _get_cross_encoder() -> CrossEncoder:
    """Lazily load the cross-encoder reranker model."""
    global _cross_encoder
    if _cross_encoder is None:
        logger.info(f"Loading cross-encoder model: {config.RERANKER_MODEL}")
        _cross_encoder = CrossEncoder(
            config.RERANKER_MODEL,
            max_length=512,
            default_activation_function=torch.nn.Sigmoid(),
        )
        logger.info("Cross-encoder loaded successfully.")
    return _cross_encoder


def _get_openai_client() -> OpenAI:
    """Return a cached OpenAI client."""
    global _openai_client
    if _openai_client is None:
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not configured.")
        _openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _openai_client


# ── Stage 1: Semantic Vector Search ──────────────────────────────────────────

def _vector_search(query_embedding: list[float], limit: int = config.VECTOR_SEARCH_LIMIT) -> list[dict]:
    """
    Perform approximate nearest-neighbor search using pgvector.
    Uses cosine distance operator (<=>).
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, content, metadata,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM documents
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                (query_embedding, query_embedding, limit),
            )
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "content": row[1],
            "metadata": row[2],
            "vector_similarity": float(row[3]),
        })

    logger.debug(f"Vector search returned {len(results)} results.")
    return results


# ── Stage 2: BM25 Keyword Search (PostgreSQL Native) ─────────────────────────

def _bm25_search(query: str, limit: int = config.BM25_SEARCH_LIMIT) -> list[dict]:
    """
    Perform full-text search using PostgreSQL tsvector/tsquery.
    Uses ts_rank_cd for relevance scoring (cover density ranking,
    which approximates BM25-style term frequency weighting).
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, content, metadata,
                       ts_rank_cd(ts_content, plainto_tsquery('english', %s)) AS rank
                FROM documents
                WHERE ts_content @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC
                LIMIT %s;
                """,
                (query, query, limit),
            )
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "content": row[1],
            "metadata": row[2],
            "bm25_rank": float(row[3]),
        })

    logger.debug(f"BM25 search returned {len(results)} results.")
    return results


# ── Stage 3: Reciprocal Rank Fusion (RRF) ────────────────────────────────────

def _reciprocal_rank_fusion(
    vector_results: list[dict],
    bm25_results: list[dict],
    k: int = config.RRF_K,
) -> list[dict]:
    """
    Combine results from multiple retrievers using RRF.
    
    Formula: score(d) = Σ 1 / (k + rank_i(d))
    
    Where k is a constant (default 60) that dampens the effect of high rankings,
    and rank_i(d) is the rank of document d in result list i (1-indexed).
    
    Returns merged results sorted by RRF score (descending).
    """
    # Build lookup: doc_id → document data
    doc_lookup: dict[int, dict] = {}
    rrf_scores: dict[int, float] = defaultdict(float)
    source_ranks: dict[int, dict] = defaultdict(dict)

    # Process vector results
    for rank, doc in enumerate(vector_results, start=1):
        doc_id = doc["id"]
        doc_lookup[doc_id] = {
            "id": doc_id,
            "content": doc["content"],
            "metadata": doc["metadata"],
        }
        rrf_scores[doc_id] += 1.0 / (k + rank)
        source_ranks[doc_id]["vector_rank"] = rank
        source_ranks[doc_id]["vector_similarity"] = doc.get("vector_similarity", 0)

    # Process BM25 results
    for rank, doc in enumerate(bm25_results, start=1):
        doc_id = doc["id"]
        if doc_id not in doc_lookup:
            doc_lookup[doc_id] = {
                "id": doc_id,
                "content": doc["content"],
                "metadata": doc["metadata"],
            }
        rrf_scores[doc_id] += 1.0 / (k + rank)
        source_ranks[doc_id]["bm25_rank"] = rank
        source_ranks[doc_id]["bm25_score"] = doc.get("bm25_rank", 0)

    # Build final list sorted by RRF score
    merged = []
    for doc_id in rrf_scores:
        entry = doc_lookup[doc_id].copy()
        entry["rrf_score"] = rrf_scores[doc_id]
        entry["source_ranks"] = source_ranks[doc_id]
        merged.append(entry)

    merged.sort(key=lambda x: x["rrf_score"], reverse=True)

    logger.debug(
        f"RRF merged {len(vector_results)} vector + {len(bm25_results)} BM25 "
        f"→ {len(merged)} unique results."
    )
    return merged


# ── Stage 4: Cross-Encoder Reranking ─────────────────────────────────────────

def _cross_encoder_rerank(
    query: str,
    candidates: list[dict],
    top_k: int = config.RERANKER_TOP_K,
) -> list[dict]:
    """
    Rerank candidates using the cross-encoder model.
    
    Scores each (query, document) pair and returns the top_k most relevant.
    Uses sigmoid activation for 0–1 normalized scores.
    """
    if not candidates:
        return []

    model = _get_cross_encoder()

    # Build pairs for cross-encoder
    pairs = [(query, doc["content"]) for doc in candidates]

    # Score all pairs
    scores = model.predict(pairs)

    # Attach scores and sort
    for doc, score in zip(candidates, scores):
        doc["reranker_score"] = float(score)

    candidates.sort(key=lambda x: x["reranker_score"], reverse=True)

    top_results = candidates[:top_k]

    logger.debug(
        f"Cross-encoder reranked {len(candidates)} candidates → top {len(top_results)}. "
        f"Score range: [{top_results[-1]['reranker_score']:.4f}, {top_results[0]['reranker_score']:.4f}]"
    )
    return top_results


# ── Main Hybrid Search Function ──────────────────────────────────────────────

def hybrid_search(query: str, top_k: int = config.RERANKER_TOP_K) -> list[dict]:
    """
    Perform hybrid search combining vector + keyword retrieval with reranking.
    
    Pipeline:
      1. Embed query → vector search (pgvector cosine, top 20)
      2. Keyword search (PostgreSQL tsvector, top 20)
      3. Reciprocal Rank Fusion to merge both sets
      4. Cross-Encoder reranking → final top_k results
    
    Args:
        query: The search query string.
        top_k: Number of final results to return (default 10).
    
    Returns:
        List of dicts, each containing:
          - content: The text chunk
          - score: Final reranker score (0–1)
          - metadata: Source file, page, chunk index
          - source_ranks: Which retrievers found it and at what rank
          - rrf_score: Intermediate RRF fusion score
          - reranker_score: Cross-encoder relevance score
    """
    logger.info(f"Hybrid search: '{query[:80]}...' (top_k={top_k})")

    # Stage 1: Embed query
    client = _get_openai_client()
    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=[query],
        dimensions=config.EMBEDDING_DIMENSIONS,
    )
    query_embedding = response.data[0].embedding

    # Stage 2: Parallel retrieval (vector + BM25)
    vector_results = _vector_search(query_embedding)
    bm25_results = _bm25_search(query)

    # Stage 3: Reciprocal Rank Fusion
    merged = _reciprocal_rank_fusion(vector_results, bm25_results)

    # Stage 4: Cross-Encoder Reranking
    final_results = _cross_encoder_rerank(query, merged, top_k=top_k)

    # Normalize output
    output = []
    for doc in final_results:
        output.append({
            "content": doc["content"],
            "score": doc["reranker_score"],
            "metadata": doc["metadata"],
            "source_ranks": doc.get("source_ranks", {}),
            "rrf_score": doc.get("rrf_score", 0),
            "reranker_score": doc["reranker_score"],
        })

    logger.info(f"Hybrid search complete: {len(output)} results returned.")
    return output


# ── Convenience: Generate Answer ──────────────────────────────────────────────

def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """
    Generate an answer using GPT-4o-mini with retrieved context.
    
    Args:
        query: User's question
        context_chunks: Results from hybrid_search()
    
    Returns:
        Generated answer string
    """
    client = _get_openai_client()

    # Build context block
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        source = chunk.get("metadata", {}).get("source_file", "Unknown")
        score = chunk.get("score", 0)
        context_parts.append(
            f"[Source {i} | {source} | Relevance: {score:.2f}]\n{chunk['content']}"
        )
    context_block = "\n\n---\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior UK financial compliance expert. Answer questions "
                "accurately based ONLY on the provided context. If the context doesn't "
                "contain enough information to answer fully, say so explicitly. "
                "Cite specific sources using [Source N] notation. "
                "Be precise about regulations, dates, and requirements."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context_block}\n\n"
                f"Question: {query}\n\n"
                "Provide a detailed, well-structured answer citing the sources."
            ),
        },
    ]

    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )

    return response.choices[0].message.content
