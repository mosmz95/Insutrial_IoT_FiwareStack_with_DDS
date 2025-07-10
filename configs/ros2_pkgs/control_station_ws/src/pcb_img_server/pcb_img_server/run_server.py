from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid

app = FastAPI()
print("hi")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded files statically
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Check if it's an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Generate a unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Save the file
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    # Return a public URL
    image_url = f"http://localhost:5000/images/{filename}"
    return {"image_url": image_url}
