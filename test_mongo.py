import asyncio
from utils.db import uploads_collection, dataset_collection

async def run():
    doc1 = {"test": "uploads"}
    doc2 = {"test": "dataset"}

    res1 = await uploads_collection.insert_one(doc1)
    res2 = await dataset_collection.insert_one(doc2)

    print("Inserted into uploads:", res1.inserted_id)
    print("Inserted into dataset:", res2.inserted_id)

    found1 = await uploads_collection.find_one({"_id": res1.inserted_id})
    found2 = await dataset_collection.find_one({"_id": res2.inserted_id})

    print("Found in uploads:", found1)
    print("Found in dataset:", found2)

asyncio.run(run())
