
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from backend.image_processing import process_image
import base64

app = FastAPI()

# Middleware to allow frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Test to check if running
@app.get("/")
def home():
    return {"message": "Trackmind backend running"}

# Uploaded image endpoint, takes image and processes it
@app.post("/upload")
async def upload_track(file: UploadFile = File(...)):
    # Reads image as bytes
    contents = await file.read()

    # Converts bytes into NumPy array
    image_array = np.frombuffer(contents, dtype=np.uint8)

    # Decodes the array into an image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Invalid image"}

    # Calls image processing func from processing file
    processed_image = process_image(image)

    # Converts processed image into PNG data
    success, encoded_image = cv2.imencode(".png", processed_image)

    if not success:
        return {"error": "Image encoding failed"}

    # Converts image into bytes
    # Bytes into base64 so its suitable for JSON
    # Base64 into a python string
    image_base64 = base64.b64encode(encoded_image.tobytes()).decode("utf-8")

    return {
        "filename": file.filename,
        "width": image.shape[1],
        "height": image.shape[0],
        "processed": True,
        "processed_image": image_base64
    }


