from pathlib import Path
from langchain_core.documents import Document

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


documents = []

for section in sections:
    title = section["title"]
    text = "\n".join(section["content"]).strip()

    # Parse structured titles such as:
    # COMMERCIAL — WORKSPACE — ENTRY
    parts = [part.strip() for part in title.split("—")]

    domain = parts[0].lower() if len(parts) > 0 else "unknown"
    service = parts[1].lower() if len(parts) > 1 else "general"
    topic = parts[2].lower() if len(parts) > 2 else "general"

    document = Document(
        page_content=f"{title}\n\n{text}",
        metadata={
            "domain": domain,
            "service": service,
            "topic": topic,
            "source": "speedlink_crm_knowledge_base"
        }
    )

    documents.append(document)


print(f"Created {len(documents)} RAG documents.")

print("\n--- FIRST 5 DOCUMENTS ---")

for i, document in enumerate(documents[:5], start=1):
    print(f"\n[{i}]")
    print("Metadata:", document.metadata)
    print("Content preview:")
    print(document.page_content[:300])