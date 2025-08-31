# utils/unsplash.py
import requests, os, io
from PIL import Image
import numpy as np
from models.embedder import get_embedding
from utils.db import dataset_collection

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def fetch_unsplash_images(category, count=100):
    url = f"https://api.unsplash.com/search/photos?query={category}&client_id={UNSPLASH_ACCESS_KEY}&count={count}"
    res = requests.get(url)
    data = res.json()
    return data.get("results", [])

async def ensure_dataset_for_category(category):
    existing = await dataset_collection.count_documents({"category": category})
    if existing >= 50:
        return

    print(f"[INFO] Fetching Unsplash images for category: {category}")
    results = fetch_unsplash_images(category, count=100)

    docs = []
    for item in results:
        try:
            img_url = item["urls"]["small"]

            # 🔑 load directly into numpy
            resp = requests.get(img_url)
            img = Image.open(io.BytesIO(resp.content)).convert("RGB")
            img = img.resize((224, 224))  # match MobileNetV2 input
            x = np.array(img)

            emb = get_embedding(x).tolist()

            docs.append({
                "id": item["id"],
                "fileName": f"{category}_{item['id']}.jpg",
                "category": category,
                "url": img_url,
                "embedding": emb,
                "alt": item.get("alt_description"),
                "likes": item.get("likes", 0)
            })
        except Exception as e:
            print("❌ Failed to process dataset image:", e)

    if docs:
        await dataset_collection.insert_many(docs)
        print(f"[INFO] Inserted {len(docs)} images for {category}")
