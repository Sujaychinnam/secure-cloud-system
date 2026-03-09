from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

import shutil
import os

from backend.crypto_engine import encrypt_file
from backend.cloud_storage import upload_file
from backend.blockchain import Blockchain

app = FastAPI()

templates = Jinja2Templates(directory="server/templates")

blockchain = Blockchain()


# =========================
# Web Dashboard
# =========================

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "chain": blockchain.chain}
    )


# =========================
# Upload API
# =========================

@app.post("/upload")
async def upload_file_api(file: UploadFile = File(...)):

    os.makedirs("storage", exist_ok=True)

    path = f"storage/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    key, encrypted = encrypt_file(path)

    cloud_name = upload_file(encrypted)

    blockchain.add_block(
        cloud_name,
        key,
        "web_user",
        "receiver"
    )

    return {"status": "uploaded", "file": cloud_name}