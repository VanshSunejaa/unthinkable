import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

UPLOADS_URI = os.getenv("MONGO_URI")
DATASET_URI = os.getenv("MONGO_DATASET_URI")

# Client for uploads DB
uploads_client = motor.motor_asyncio.AsyncIOMotorClient(UPLOADS_URI)
uploads_db = uploads_client.get_database("uploads_db")
uploads_collection = uploads_db["products"]

# Client for dataset DB
dataset_client = motor.motor_asyncio.AsyncIOMotorClient(DATASET_URI)
dataset_db = dataset_client.get_database("dataset_db")
dataset_collection = dataset_db["products"]
