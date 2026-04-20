import chromadb

DOCS = [
    {"id": "1", "text": "RAG stands for Retrieval-Augmented Generation. It combines a retriever with a language model."},
    {"id": "2", "text": "Chroma is an open-source vector database designed for AI applications."},
    {"id": "3", "text": "Embeddings are numerical representations of text that capture semantic meaning."},
    {"id": "4", "text": "Vector search finds documents by similarity in embedding space rather than keyword matching."},
    {"id": "5", "text": "LangChain and LlamaIndex are popular frameworks for building RAG pipelines."},
]

QUERY = "How does retrieval work in AI systems?"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("rag-example")

collection.upsert(
    ids=[d["id"] for d in DOCS],
    documents=[d["text"] for d in DOCS],
)

print("=== Ingested documents ===")
for d in DOCS:
    print(f"  [{d['id']}] {d['text']}")

print(f"\n=== Query ===")
print(f"  {QUERY}")

results = collection.query(query_texts=[QUERY], n_results=3)

print("\n=== Top 3 results ===")
for i, (doc, dist) in enumerate(zip(results["documents"][0], results["distances"][0]), 1):
    print(f"  {i}. (distance={dist:.4f}) {doc}")
