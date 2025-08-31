import os, json
from models.embedder import get_embedding
from utils.db import products_collection
import asyncio

async def seed():
    products = []
    images_path = "data/images"
    for img_name in os.listdir(images_path)[:50]:  # take first 50
        path = os.path.join(images_path, img_name)
        emb = get_embedding(path).tolist()
        products.append({
            "fileName": img_name,
            "path": path,
            "embedding": emb,
            "category": "Clothing"
        })

    await products_collection.insert_many(products)
    print("Inserted", len(products), "products")

if __name__ == "__main__":
    asyncio.run(seed())
