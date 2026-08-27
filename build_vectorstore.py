from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


KB_PATH = Path("data/speedlink_crm_knowledge_base.md")


# ---------- Load Markdown ----------

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


# ---------- Create structured Documents ----------

documents = []

for section in sections:
    title = section["title"]
    text = "\n".join(section["content"]).strip()

    parts = [part.strip() for part in title.split("—")]

    domain = parts[0].lower() if len(parts) > 0 else "unknown"
    service_raw = parts[1].lower() if len(parts) > 1 else "general"
    topic = parts[2].lower() if len(parts) > 2 else "general"

    # Normalize workspace service names
    service = service_raw
    service_type = "general"

    if service_raw.startswith("workspace (") and service_raw.endswith(")"):
        service = "workspace"
        service_type = service_raw[11:-1].strip()

    document = Document(
        page_content=f"{title}\n\n{text}",
        metadata={
            "domain": domain,
            "service": service,
            "service_type": service_type,
            "topic": topic,
            "source": "speedlink_crm_knowledge_base"
        }
    )

    documents.append(document)


# ---------- Create embedding model ----------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------- Build FAISS ----------

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)


# ---------- Save ----------

vectorstore.save_local("vectorstore")


print("Vector store rebuilt successfully.")
print(f"Documents indexed: {len(documents)}")

print("\n--- SAMPLE METADATA ---")

for document in documents[4:10]:
    print(document.metadata)