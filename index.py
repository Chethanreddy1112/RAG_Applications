import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

with open("scraped_data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]

metadatas = [
    {
        "card_name": c["card_name"],
        "category": c["category"],
        "source": c["source"]
    }
    for c in chunks
]

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

db = Chroma.from_texts(
    texts=texts,
    embedding=embedding,
    metadatas=metadatas,
    persist_directory="chroma_db"
)

db.persist()

print("Vector DB Created")