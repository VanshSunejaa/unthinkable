# routes/similar.py
from fastapi import APIRouter, Query
import numpy as np
from bson import ObjectId
from utils.db import uploads_collection, dataset_collection

router = APIRouter()


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors"""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.get("/similar")
async def find_similar(fileName: str = Query(...)):
    # 1. Find the uploaded image embedding
    uploaded = await uploads_collection.find_one({"fileName": fileName})
    if not uploaded:
        return {"error": "File not found in uploads DB"}

    upload_emb = uploaded["embedding"]
    category = uploaded["category"]

    # 2. Fetch dataset for the same category
    dataset_cursor = dataset_collection.find({"category": category})
    dataset = await dataset_cursor.to_list(length=200)  # fetch up to 200 docs

    # 3. Compute similarities
    results = []
    for item in dataset:
        try:
            sim = cosine_similarity(upload_emb, item["embedding"])
            results.append({
                "fileName": item["fileName"],
                "url": item.get("url"),   # Unsplash URL (if saved)
                "score": sim,
                "category": category
            })
        except Exception as e:
            print("❌ Similarity error:", e)

    # 4. Sort by score and return top 50
    results = sorted(results, key=lambda x: x["score"], reverse=True)[:50]

    return {"similar": results}
