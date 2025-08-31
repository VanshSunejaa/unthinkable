# models/embedder.py
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os

# embedding model
embedding_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")

# classification model
classification_model = MobileNetV2(weights="imagenet")

def _load_img(img_input):
    """
    Helper to load image from path, URL, or numpy array.
    Returns numpy array ready for model.
    """
    if isinstance(img_input, str):
        if img_input.startswith("http://") or img_input.startswith("https://"):
            # URL input
            response = requests.get(img_input, timeout=10)
            if response.status_code != 200:
                raise ValueError("Could not fetch image from URL")
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img = img.resize((224, 224))
            x = np.array(img)
        elif os.path.exists(img_input):
            # Local file path
            img = image.load_img(img_input, target_size=(224, 224))
            x = image.img_to_array(img)
        else:
            raise ValueError("Invalid file path or URL")
    elif isinstance(img_input, np.ndarray):
        if img_input.shape[:2] != (224, 224):
            img = Image.fromarray(img_input.astype("uint8")).resize((224, 224))
            x = np.array(img)
        else:
            x = img_input
    else:
        raise ValueError("Unsupported input type for image")

    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def get_embedding(img_input):
    """
    Return 1280-dim embedding for an image.
    Accepts file path, URL, or numpy array.
    """
    x = _load_img(img_input)
    return embedding_model.predict(x)[0]


def get_category(img_input):
    """
    Predict category label from image path or URL.
    Returns top-1 ImageNet label.
    """
    x = _load_img(img_input)
    preds = classification_model.predict(x)
    decoded = decode_predictions(preds, top=1)[0]
    return decoded[0][1]  # return label string
