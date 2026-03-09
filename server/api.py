from fastapi import FastAPI, UploadFile
import shutil

from backend.crypto_engine import encrypt_file
from backend.cloud_storage import upload_file
from backend.blockchain import Blockchain

app = FastAPI()

blockchain = Blockchain()


@app.get("/")
def root():
    return {"message":"Secure Cloud API running"}


@app.post("/upload/")
async def upload(file: UploadFile):

    path = f"storage/{file.filename}"

    with open(path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    key, encrypted_file = encrypt_file(path)

    cloud_name = upload_file(encrypted_file)

    blockchain.add_block(
        cloud_name,
        key,
        "api_user",
        "receiver"
    )

    return {"file":cloud_name}