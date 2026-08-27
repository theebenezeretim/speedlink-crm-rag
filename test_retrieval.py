from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


query = "I need somewhere to work for a few hours"

print(f"QUERY: {query}\n")

results = vectorstore.similarity_search(query, k=5)

for i, document in enumerate(results, start=1):
    print(f"--- RESULT {i} ---")
    print(f"Domain: {document.metadata['domain']}")
    print(f"Service: {document.metadata['service']}")
    print(f"Service Type: {document.metadata['service_type']}")
    print(f"Topic: {document.metadata['topic']}")
    print()
    print(document.page_content[:400])
    print()