# routes/upload.py
from fastapi import APIRouter, UploadFile, File, Form
import shutil, os
from typing import Optional
from models.embedder import get_embedding, get_category
from utils.db import uploads_collection, dataset_collection
from utils.unsplash import ensure_dataset_for_category
from routes.similar import find_similar
import requests
from io import BytesIO

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_image(
    image: Optional[UploadFile] = File(None),
    fileName: str = Form(...),
    url: Optional[str] = Form(None)
):
    """
    Upload an image either by file or by URL.
    - If `image` is provided, save locally.
    - If `url` is provided, download/embed directly, store URL in DB.
    """

    file_path = None
    final_url = None

    # 1. Handle file upload
    if image is not None:
        file_path = os.path.join(UPLOAD_DIR, fileName)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # 2. Handle URL upload
    elif url:
        final_url = url
        # Download temp file for embedding only
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"success": False, "error": "Could not fetch image from URL"}
        tmp_path = os.path.join(UPLOAD_DIR, f"tmp_{fileName}")
        with open(tmp_path, "wb") as f:
            f.write(response.content)
        file_path = tmp_path  # use temp file for embedding

    else:
        return {"success": False, "error": "No file or URL provided"}

    # 3. Get embedding + category
    embedding = get_embedding(file_path).tolist()
    category = get_category(file_path)

    # Remove temp file if created from URL
    if final_url and file_path and file_path.startswith("uploads/tmp_"):
        try:
            os.remove(file_path)
        except:
            pass

    # 4. Store upload info in DB
    product = {
        "fileName": fileName,
        "embedding": embedding,
        "category": category
    }
    if final_url:
        product["url"] = final_url
    else:
        product["path"] = file_path

    result = await uploads_collection.insert_one(product)

    print(f"[UPLOAD] Detected category: {category}")

    # 5. Ensure dataset exists for this category
    dataset_images = await ensure_dataset_for_category(category)

    # 6. Fallback: fetch dataset from DB
    if dataset_images is None:
        dataset_images = await dataset_collection.find(
            {"category": category},
            {"_id": 0, "fileName": 1, "url": 1, "category": 1}
        ).to_list(length=10)

    return {
        "success": True,
        "data": {
            "id": str(result.inserted_id),
            "fileName": fileName,
            "category": category,
            "dataset": dataset_images
        }
    }
