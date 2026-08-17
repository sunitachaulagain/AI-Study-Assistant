from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Machine learning can be used to predict high-risk accident zones."

embedding = model.encode(text)

print("Embedding type:", type(embedding))
print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])