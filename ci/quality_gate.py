"""
CI/CD Quality Gate — Fails the build if RAGAS scores are below thresholds.

Reads evaluation/results/results.json and:
  - Exits with code 0 if both faithfulness >= 0.85 AND relevancy >= 0.85
  - Exits with code 1 if either score is below threshold
"""

import json
import logging
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("quality_gate")

# Thresholds
FAITHFULNESS_THRESHOLD = 0.85
RELEVANCY_THRESHOLD = 0.85

# Default results path
DEFAULT_RESULTS_PATH = Path(__file__).parent.parent / "evaluation" / "results" / "results.json"


def run_quality_gate(results_path: str | Path | None = None) -> bool:
    """
    Read evaluation results and check against quality thresholds.
    
    Args:
        results_path: Path to results.json. Defaults to evaluation/results/results.json
    
    Returns:
        True if quality thresholds are met, False otherwise.
    """
    results_path = Path(results_path or DEFAULT_RESULTS_PATH)

    logger.info(f"Quality Gate — {datetime.now(timezone.utc).isoformat()}")
    logger.info(f"Reading results from: {results_path}")

    # ── Read Results ──────────────────────────────────────────────────────
    if not results_path.exists():
        logger.error(f"Results file not found: {results_path}")
        logger.error("Run the evaluation pipeline first: python -m evaluation.evaluate_pipeline")
        return False

    try:
        with open(results_path, "r") as f:
            results = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in results file: {e}")
        return False

    # ── Extract Scores ────────────────────────────────────────────────────
    faithfulness = results.get("faithfulness")
    relevancy = results.get("answer_relevancy")

    if faithfulness is None or relevancy is None:
        logger.error(
            f"Missing required fields in results.json. "
            f"Found keys: {list(results.keys())}"
        )
        return False

    logger.info(f"Faithfulness Score    : {faithfulness:.4f}  (threshold: {FAITHFULNESS_THRESHOLD})")
    logger.info(f"Answer Relevancy     : {relevancy:.4f}  (threshold: {RELEVANCY_THRESHOLD})")
    logger.info(f"Evaluation Timestamp : {results.get('timestamp', 'N/A')}")
    logger.info(f"Questions Evaluated  : {results.get('total_questions', 'N/A')}")

    # ── Check Thresholds ──────────────────────────────────────────────────
    failures = []
    if faithfulness < FAITHFULNESS_THRESHOLD:
        failures.append(
            f"Faithfulness {faithfulness:.4f} < {FAITHFULNESS_THRESHOLD}"
        )
    if relevancy < RELEVANCY_THRESHOLD:
        failures.append(
            f"Answer Relevancy {relevancy:.4f} < {RELEVANCY_THRESHOLD}"
        )

    if failures:
        logger.error("=" * 50)
        logger.error("  QUALITY GATE — FAILED")
        logger.error("=" * 50)
        for failure in failures:
            logger.error(f"  ✗ {failure}")
        logger.error("=" * 50)
        return False

    logger.info("=" * 50)
    logger.info("  QUALITY GATE — Quality Threshold Passed")
    logger.info("=" * 50)
    return True


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Optional: pass results path as CLI argument
    results_file = sys.argv[1] if len(sys.argv) > 1 else None
    passed = run_quality_gate(results_file)
    sys.exit(0 if passed else 1)
