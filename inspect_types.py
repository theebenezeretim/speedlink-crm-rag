from pathlib import Path
from collections import Counter
import re


KB_PATH = Path("data/speedlink_crm_knowledge_base.md")

content = KB_PATH.read_text(encoding="utf-8")

types = re.findall(r"\*\*Type:\*\*\s*(.+)", content)

counts = Counter(types)

print("Knowledge Base Types")
print("=" * 40)

for document_type, count in counts.items():
    print(f"{document_type}: {count}")

print(f"\nTotal typed sections: {sum(counts.values())}")