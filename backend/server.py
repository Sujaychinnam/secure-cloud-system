from fastapi import FastAPI, UploadFile
import shutil
import os

app = FastAPI()

STORAGE = "storage"

os.makedirs(STORAGE, exist_ok=True)

@app.post("/upload")

async def upload(file: UploadFile):

    path = f"{STORAGE}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"status":"stored"}