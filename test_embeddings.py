from langchain_huggingface import HuggingFaceEmbeddings


model = HuggingFaceEmbeddings(
	model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text = "I need a place to work for a few hours."

embedding = model.embed_query(text)

print("Embedding created successfully.")
print(f"Number of dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
