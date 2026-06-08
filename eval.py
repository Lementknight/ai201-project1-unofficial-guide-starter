#!/usr/bin/env python3
"""
Evaluation script: Run all 6 test questions and log results to EVALUATION_PROGRESS.md
Tracks improvements over multiple runs with corpus status and changes documented.
"""

import json
from datetime import datetime
from pathlib import Path

from embed import load_chunks
from query import ask

# 6 evaluation questions with expected answers
EVAL_QUESTIONS = [
    {
        "id": 1,
        "question": "Why should someone choose to max out their medical FSA account?",
        "expected": "You should max out your medical FSA only if you have predictable medical expenses (prescriptions, glasses, copays) that you'll incur within the plan year, because contributions are pre-tax. However, medical FSAs have a strict 'use it or lose it' rule—unused money is forfeited (though some employers allow a small grace period or up to $610 carryover in 2026)—so you shouldn't max out if you're uncertain about expenses.",
    },
    {
        "id": 2,
        "question": "If my stocks at a company mature only after 5 years, do I need to remain with the company to get my money's worth?",
        "expected": "Yes, you must remain with the company until the shares vest (mature). If you leave before 5 years, unvested shares are forfeited and you lose that equity compensation. However, once shares vest and are delivered to you, you own them and they can't be clawed back if you leave.",
    },
    {
        "id": 3,
        "question": "If I am already covered for health insurance, should I even consider enrolling in my company's plan?",
        "expected": "Yes, you should consider enrolling in your company's plan because employer plans typically offer better coverage and lower costs than individual plans, plus employers often contribute to premiums, deductibles, or HSA/FSA accounts. You may also face coordination-of-benefits questions and tax implications.",
    },
    {
        "id": 4,
        "question": "What is open enrollment?",
        "expected": "Open enrollment is the annual period (typically once per year, often in the fall) when employees can enroll in, change, or drop their benefits plans. Outside of open enrollment, you can only change elections if you experience a qualifying life event (marriage, birth, job loss, etc.).",
    },
    {
        "id": 5,
        "question": "What is the difference between PTO, short-term disability, and long-term disability?",
        "expected": "PTO (paid time off) covers vacation, sick days, and personal days that you can use at your discretion. Short-term disability replaces a portion of your salary when a medical issue prevents you from working, typically lasting weeks to months. Long-term disability replaces a portion of salary for longer absences, starting when short-term disability ends and potentially lasting until retirement.",
    },
    {
        "id": 6,
        "question": "What is the advantage of using commuter benefits instead of paying for transit or parking out of pocket?",
        "expected": "Commuter benefits allow you to pay for public transit, parking, or vanpool costs with pre-tax dollars, reducing your taxable income and saving on taxes. Unlike medical FSAs, commuter benefit plans often allow unused funds to roll over to the next year (check your plan), making them a lower-risk savings option for predictable commuting costs.",
    },
]


def get_corpus_status() -> dict:
    """
    Analyze current corpus: number of chunks, sources included.
    Returns dict with corpus metadata.
    """
    try:
        chunks = load_chunks()
        sources = {}
        for chunk in chunks:
            url = chunk["source_url"]
            if url not in sources:
                sources[url] = 0
            sources[url] += 1

        return {
            "total_chunks": len(chunks),
            "sources": sources,
            "num_sources": len(sources),
        }
    except FileNotFoundError:
        return {
            "total_chunks": 0,
            "sources": {},
            "num_sources": 0,
        }


def run_evaluation() -> list[dict]:
    """
    Run all 6 evaluation questions and collect responses.
    Returns list of dicts with: id, question, expected, response, sources
    """
    results = []

    print("=" * 80)
    print(f"EVALUATION RUN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    for i, q in enumerate(EVAL_QUESTIONS, 1):
        print(f"[{i}/6] {q['question']}")
        print()

        answer, sources = ask(q["question"])

        results.append(
            {
                "id": q["id"],
                "question": q["question"],
                "expected": q["expected"],
                "response": answer,
                "sources": sources,
            }
        )

        print(f"RESPONSE:\n{answer}\n")
        print(f"SOURCES:\n{sources}\n")
        print("-" * 80)
        print()

    return results


def format_run_for_markdown(
    results: list[dict],
    run_number: int,
    timestamp: str,
    corpus_status: dict,
    changes: str = "No changes documented",
) -> str:
    """
    Format evaluation results as markdown for EVALUATION_PROGRESS.md
    Includes corpus status and changes made since last run.
    """
    md = f"\n## Run #{run_number} — {timestamp}\n\n"

    # Corpus status
    md += "### Corpus Status\n"
    md += f"- **Total chunks:** {corpus_status['total_chunks']}\n"
    md += f"- **Sources ingested:** {corpus_status['num_sources']}\n"
    md += "- **Sources breakdown:**\n"
    for url, count in sorted(corpus_status["sources"].items()):
        md += f"  - `{count}` chunks from {url[:60]}...\n"
    md += "\n"

    # Changes since last run
    md += "### Changes Since Last Run\n"
    md += f"{changes}\n\n"

    # Results
    md += "### Evaluation Results\n\n"

    for result in results:
        md += f"#### Q{result['id']}: {result['question']}\n\n"
        md += f"**Expected:**\n> {result['expected']}\n\n"
        md += f"**System Response:**\n> {result['response']}\n\n"
        md += f"**Sources Cited:**\n{result['sources']}\n\n"

    return md


def append_to_progress_md(
    results: list[dict], corpus_status: dict, changes: str = "No changes documented"
):
    """
    Append evaluation results to EVALUATION_PROGRESS.md with timestamp, corpus status, and changes.
    Creates file if it doesn't exist.
    """
    progress_file = Path("EVALUATION_PROGRESS.md")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Determine run number and create/append
    if progress_file.exists():
        with open(progress_file, "r") as f:
            content = f.read()
        # Count existing runs
        run_number = content.count("## Run #") + 1
    else:
        run_number = 1
        # Create header
        with open(progress_file, "w") as f:
            f.write("# Evaluation Progress Log\n\n")
            f.write(
                "## Overview\n"
                "This document tracks how the RAG system improves over time.\n\n"
                "Each run includes:\n"
                "- **Corpus Status:** How many chunks, from which sources\n"
                "- **Changes Since Last Run:** What was modified to improve results\n"
                "- **Evaluation Results:** Responses to all 6 test questions with expected vs. actual\n\n"
            )
            f.write(
                "**Key Note:** Early runs may have poor performance due to incomplete corpus "
                "(some sources couldn't be scraped with basic HTTP requests). "
                "As sources are added via improved scraping (e.g., Playwright for JavaScript-heavy sites), "
                "accuracy improves.\n\n"
            )

    # Append new results
    run_markdown = format_run_for_markdown(results, run_number, timestamp, corpus_status, changes)

    with open(progress_file, "a") as f:
        f.write(run_markdown)

    print(f"\n✓ Results appended to EVALUATION_PROGRESS.md (Run #{run_number})")
    print(f"  Timestamp: {timestamp}")
    print(f"  Corpus: {corpus_status['total_chunks']} chunks from {corpus_status['num_sources']} sources")


def main():
    """
    Main evaluation loop: run questions, capture corpus status, save results, show summary.
    """
    print("\n" + "=" * 80)
    print("RAG SYSTEM EVALUATION")
    print("=" * 80)
    print("\nStarting evaluation...")
    print("This will run all 6 test questions through the RAG pipeline.\n")

    # Get corpus status before running
    corpus_status = get_corpus_status()
    print(f"Current corpus: {corpus_status['total_chunks']} chunks from {corpus_status['num_sources']} sources\n")

    # Run evaluation
    results = run_evaluation()

    # Prompt for changes description
    print("\n" + "=" * 80)
    print("DOCUMENT CHANGES")
    print("=" * 80)
    changes = input(
        "\nBriefly describe what changed since the last run (e.g., 'Added Playwright for JS scraping').\n"
        "Press Enter to skip: "
    ).strip()

    if not changes:
        changes = "No changes documented"

    # Save to EVALUATION_PROGRESS.md
    append_to_progress_md(results, corpus_status, changes)

    # Print summary
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80)
    print(f"Tested 6 questions")
    print(f"Corpus: {corpus_status['total_chunks']} chunks from {corpus_status['num_sources']} sources")
    print("Results saved to EVALUATION_PROGRESS.md")
    print("\nTo view full results: cat EVALUATION_PROGRESS.md")


if __name__ == "__main__":
    main()
