import json
import chromadb

from sentence_transformers import SentenceTransformer


# CREATE CHROMA CLIENT
client = chromadb.PersistentClient(path="data/chroma_db")


# DELETE OLD COLLECTION IF EXISTS
try:
    client.delete_collection("shl_assessments")
except:
    pass


# CREATE NEW COLLECTION
collection = client.get_or_create_collection(
    name="shl_assessments"
)


# LOAD EMBEDDING MODEL
model = SentenceTransformer("all-MiniLM-L6-v2")


# LOAD CATALOG DATA
with open("data/catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)


# ADD DATA TO VECTOR DATABASE
for idx, item in enumerate(assessments):

    text = f"""
    Assessment Name:
    {item['name']}

    Description:
    {item['description']}
    """

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(idx)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{
            "name": item["name"],
            "url": item["url"]
        }]
    )

    print(f"Added {idx + 1}: {item['name']}")


print("\nVECTOR DATABASE READY")