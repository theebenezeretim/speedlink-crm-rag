"""Run repeatable source-retrieval checks; no Groq calls or API key needed."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time

from evaluation_cases import CASES
from parse_kb import load_documents
from retrieval import Retriever


def evaluate(mode="hybrid"):
    retriever = Retriever(load_documents(), mode=mode)
    results = []
    started = time.monotonic()
    for item in CASES:
        result = retriever.search(item["question"], item["history"])
        found = any(
            doc.metadata["service"] == item["service"] and doc.metadata["topic"] == item["topic"]
            and (item["kind"] is None or doc.metadata["service_type"] == item["kind"])
            for doc in result.documents[:item["top"]]
        )
        results.append({**item, "passed": found, "routed_services": result.services,
                        "retrieved": [doc.metadata["title"] for doc in result.documents]})
    return {"requested_mode": mode, "actual_mode": retriever.mode, "warning": retriever.warning,
            "passed": sum(row["passed"] for row in results), "total": len(results),
            "seconds": round(time.monotonic() - started, 2),
            "indexed_sections": dict(Counter(d.metadata["service"] for d in retriever.documents)),
            "cases": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("hybrid", "lexical"), default="hybrid")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate(args.mode)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{report['passed']}/{report['total']} passed; mode={report['actual_mode']}; {report['seconds']}s")
    for row in report["cases"]:
        if not row["passed"]:
            print("FAIL:", row["question"], "expected", row["service"], row["kind"], row["topic"])
            print("  Retrieved:", row["retrieved"][:row["top"]])
    if report["warning"]:
        print(report["warning"])
    raise SystemExit(0 if report["passed"] == report["total"] and report["actual_mode"] == args.mode else 1)


if __name__ == "__main__":
    main()
