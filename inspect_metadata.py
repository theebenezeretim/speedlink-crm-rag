from pathlib import Path
from collections import defaultdict


KB_PATH = Path("data/speedlink_crm_knowledge_base.md")

content = KB_PATH.read_text(encoding="utf-8")

sections = []
current_section = None

for line in content.splitlines():
    if line.startswith("## "):
        if current_section:
            sections.append(current_section)

        current_section = {
            "title": line[3:].strip(),
            "content": []
        }

    elif current_section:
        current_section["content"].append(line)

if current_section:
    sections.append(current_section)


metadata = defaultdict(set)

for section in sections:
    parts = [part.strip() for part in section["title"].split("—")]

    domain = parts[0].lower() if len(parts) > 0 else "unknown"
    service = parts[1].lower() if len(parts) > 1 else "general"
    topic = parts[2].lower() if len(parts) > 2 else "general"

    metadata[domain].add((service, topic))


for domain, items in metadata.items():
    print(f"\n{'=' * 60}")
    print(f"DOMAIN: {domain}")
    print(f"{'=' * 60}")

    for service, topic in sorted(items):
        print(f"- {service} → {topic}")