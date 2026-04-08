"""
RAGAS Evaluation Pipeline for the Legal RAG System.

Runs the full RAG pipeline against the golden dataset,
calculates Faithfulness and Answer Relevancy scores,
and exports results for CI/CD gating.
"""

import json
import logging
import os
import time
from pathlib import Path

import pandas as pd
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy
from ragas import EvaluationDataset, SingleTurnSample
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from evaluation.golden_dataset import get_golden_dataset
from engine.hybrid_search import hybrid_search, generate_answer

logger = logging.getLogger(__name__)

# Output directory
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def run_rag_pipeline(questions: list[str]) -> list[dict]:
    """
    Run the full RAG pipeline for a list of questions.
    
    For each question:
      1. hybrid_search() → top 10 context chunks
      2. generate_answer() → LLM response using those chunks
    
    Returns:
        List of dicts with 'question', 'contexts', 'answer'
    """
    results = []
    total = len(questions)

    for i, question in enumerate(questions, 1):
        logger.info(f"[{i}/{total}] Processing: {question[:60]}...")

        try:
            # Retrieve context
            search_results = hybrid_search(question, top_k=10)
            contexts = [r["content"] for r in search_results]

            # Generate answer
            answer = generate_answer(question, search_results)

            results.append({
                "question": question,
                "contexts": contexts,
                "answer": answer,
            })

        except Exception as e:
            logger.error(f"Error processing question {i}: {e}")
            results.append({
                "question": question,
                "contexts": [],
                "answer": f"Error: {str(e)}",
            })

        # Small delay to avoid rate limiting
        time.sleep(0.5)

    return results


def build_evaluation_dataset(
    pipeline_results: list[dict],
    golden_data: list[dict],
) -> EvaluationDataset:
    """
    Build a RAGAS EvaluationDataset from pipeline results and golden ground truths.
    """
    samples = []
    for result, golden in zip(pipeline_results, golden_data):
        sample = SingleTurnSample(
            user_input=result["question"],
            retrieved_contexts=result["contexts"],
            response=result["answer"],
            reference=golden["ground_truth"],
        )
        samples.append(sample)

    return EvaluationDataset(samples=samples)


def run_evaluation() -> dict:
    """
    Full evaluation pipeline:
      1. Load golden dataset
      2. Run RAG pipeline against all questions
      3. Evaluate with RAGAS (Faithfulness + Answer Relevancy)
      4. Export results to CSV and JSON
      5. Print summary
    
    Returns:
        dict with average scores and per-question results
    """
    logger.info("=" * 60)
    logger.info("RAGAS EVALUATION PIPELINE — Starting")
    logger.info("=" * 60)

    # 1. Load golden dataset
    golden_data = get_golden_dataset()
    questions = [item["question"] for item in golden_data]
    logger.info(f"Loaded {len(golden_data)} golden dataset questions.")

    # 2. Run RAG pipeline
    logger.info("Running RAG pipeline against golden dataset...")
    t_start = time.time()
    pipeline_results = run_rag_pipeline(questions)
    pipeline_time = time.time() - t_start
    logger.info(f"Pipeline completed in {pipeline_time:.1f}s")

    # 3. Build evaluation dataset
    eval_dataset = build_evaluation_dataset(pipeline_results, golden_data)

    # 4. Configure RAGAS evaluator with OpenAI
    evaluator_llm = LangchainLLMWrapper(
        ChatOpenAI(
            model="gpt-4o-mini",
            api_key=config.OPENAI_API_KEY,
            temperature=0,
        )
    )
    evaluator_embeddings = LangchainEmbeddingsWrapper(
        OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            api_key=config.OPENAI_API_KEY,
        )
    )

    metrics = [
        Faithfulness(llm=evaluator_llm),
        AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
    ]

    # 5. Run RAGAS evaluation
    logger.info("Running RAGAS evaluation (this may take several minutes)...")
    t_eval = time.time()
    ragas_results = evaluate(
        dataset=eval_dataset,
        metrics=metrics,
    )
    eval_time = time.time() - t_eval
    logger.info(f"RAGAS evaluation completed in {eval_time:.1f}s")

    # 6. Extract results
    results_df = ragas_results.to_pandas()

    # Calculate averages
    avg_faithfulness = results_df["faithfulness"].mean()
    avg_relevancy = results_df["answer_relevancy"].mean()

    # 7. Export per-question results to CSV
    csv_path = RESULTS_DIR / "evaluation_results.csv"
    results_df.to_csv(csv_path, index=False)
    logger.info(f"Per-question results exported to: {csv_path}")

    # 8. Export summary to JSON (for CI/CD gate)
    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_questions": len(golden_data),
        "faithfulness": round(float(avg_faithfulness), 4),
        "answer_relevancy": round(float(avg_relevancy), 4),
        "pipeline_time_s": round(pipeline_time, 1),
        "evaluation_time_s": round(eval_time, 1),
        "thresholds": {
            "faithfulness": config.FAITHFULNESS_THRESHOLD,
            "answer_relevancy": config.RELEVANCY_THRESHOLD,
        },
        "passed": (
            avg_faithfulness >= config.FAITHFULNESS_THRESHOLD
            and avg_relevancy >= config.RELEVANCY_THRESHOLD
        ),
    }

    json_path = RESULTS_DIR / "results.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Summary exported to: {json_path}")

    # 9. Print summary
    print("\n" + "=" * 60)
    print("  RAGAS EVALUATION SUMMARY")
    print("=" * 60)
    print(f"  Questions Evaluated : {summary['total_questions']}")
    print(f"  Faithfulness        : {summary['faithfulness']:.4f}  (threshold: {config.FAITHFULNESS_THRESHOLD})")
    print(f"  Answer Relevancy    : {summary['answer_relevancy']:.4f}  (threshold: {config.RELEVANCY_THRESHOLD})")
    print(f"  Pipeline Time       : {summary['pipeline_time_s']}s")
    print(f"  Evaluation Time     : {summary['evaluation_time_s']}s")
    print(f"  Status              : {'✅ PASSED' if summary['passed'] else '❌ FAILED'}")
    print("=" * 60 + "\n")

    return summary


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    run_evaluation()
