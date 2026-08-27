from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from route_query import detect_service


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)


def retrieve(query, k=5):
    service = detect_service(query)

    # Retrieve more candidates first
    candidates = vectorstore.similarity_search(
        query,
        k=10,
        filter={"service": service}
    )

    # CRM workflow priority
    priority = {
        "WORKFLOW": 3,
        "DECISION_LOGIC": 3,
        "RESPONSE_TEMPLATE": 2,
        "CONDITION": 2,
        "QUALIFICATION_REQUIREMENT": 2,
        "PRICING": 1,
        "FACT": 1,
        "BUSINESS_RULE": 2,
        "PAYMENT_INFORMATION": 1,
        "FOLLOW_UP": 1,
        "OUTCOME": 1,
    }

    scored = []

    for document in candidates:
        page_content = document.page_content

        document_type = "FACT"

        for possible_type in priority:
            if f"**Type:** {possible_type}" in page_content:
                document_type = possible_type
                break

        score = priority.get(document_type, 1)

        scored.append((score, document))

    scored.sort(key=lambda item: item[0], reverse=True)

    return service, [document for _, document in scored[:k]]


query = "I need somewhere to work for a few hours"

service, results = retrieve(query)

print(f"QUERY: {query}")
print(f"SERVICE: {service}\n")

for i, document in enumerate(results, start=1):
    print(f"--- RESULT {i} ---")
    print(f"Service: {document.metadata['service']}")
    print(f"Service Type: {document.metadata['service_type']}")
    print(f"Topic: {document.metadata['topic']}")

    for line in document.page_content.splitlines():
        if line.startswith("**Type:**"):
            print(line)
            break

    print()
    print(document.page_content[:500])
    print()