"""Optional FAISS export for inspection; the app indexes current Markdown in memory."""
from pathlib import Path

from parse_kb import ROOT, load_documents
from retrieval import EMBEDDING_MODEL


def build(output: Path = ROOT / "generated_vectorstore"):
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    documents = load_documents()
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(str(output))
    print(f"Exported {len(documents)} sections to {output}")
    print("The chatbot reads the current Markdown directly; this export is not required.")


if __name__ == "__main__":
    build()
