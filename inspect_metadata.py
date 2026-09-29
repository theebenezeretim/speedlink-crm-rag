"""Inspect the same normalized metadata that the app actually uses."""
from collections import defaultdict
from parse_kb import load_documents

if __name__ == "__main__":
    grouped = defaultdict(list)
    for document in load_documents():
        grouped[document.metadata["service"]].append(document.metadata)
    for service, sections in sorted(grouped.items()):
        print(f"\n{service} ({len(sections)})")
        for section in sections:
            print(f"  {section['service_type']} / {section['topic']} [{section['type']}]")
