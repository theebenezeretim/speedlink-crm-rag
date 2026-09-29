"""One parser shared by retrieval, diagnostics, and index exports."""
from collections import Counter
from pathlib import Path
import re

from langchain_core.documents import Document

ROOT = Path(__file__).resolve().parent
KB_PATH = ROOT / "data" / "speedlink_crm_knowledge_base.md"


def parse_knowledge_base(content: str) -> list[Document]:
    documents = []
    matches = list(re.finditer(r"^## (.+)$", content, re.MULTILINE))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        parts = [part.strip().lower() for part in title.split("—")]
        if len(parts) != 3:
            continue  # File metadata is not customer-facing evidence.
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        body = content[match.end():end].strip()
        body = re.split(r"^# ", body, maxsplit=1, flags=re.MULTILINE)[0].strip()
        body = body.rstrip("-\n ")
        domain, raw_service, topic = parts
        service_type = "general"
        service = raw_service
        if domain == "research":
            service = "research"
        elif raw_service.startswith("workspace (") and raw_service.endswith(")"):
            service = "workspace"
            service_type = raw_service[len("workspace ("):-1]
        elif raw_service in {"global", "objection handling", "follow-up system"}:
            service = "general"
        kind = re.search(r"\*\*Type:\*\*\s*(\w+)", body)
        if not kind:
            raise ValueError(f"Missing Type in knowledge-base section: {title}")
        doc_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        documents.append(Document(page_content=f"{title}\n\n{body}", metadata={
            "id": doc_id, "title": title, "domain": domain,
            "service": service, "service_type": service_type, "topic": topic,
            "category": raw_service, "type": kind.group(1),
            "source": "data/speedlink_crm_knowledge_base.md",
            "line": content[:match.start()].count("\n") + 1,
        }))
    if not documents:
        raise ValueError("No structured CRM sections found in the knowledge base.")
    if len({doc.metadata["id"] for doc in documents}) != len(documents):
        raise ValueError("Duplicate knowledge-base section titles found.")
    return documents


def load_documents(path: Path = KB_PATH) -> list[Document]:
    return parse_knowledge_base(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    documents = load_documents()
    print(f"Created {len(documents)} CRM documents.")
    for service, count in sorted(Counter(d.metadata["service"] for d in documents).items()):
        print(f"{service}: {count}")
