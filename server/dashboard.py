from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from backend.blockchain import Blockchain

app = FastAPI()

blockchain = Blockchain()


@app.get("/explorer", response_class=HTMLResponse)
def explorer():

    html = "<h1>Blockchain Explorer</h1>"

    for block in blockchain.chain:

        html += f"""
        <div style="border:1px solid gray;padding:10px;margin:10px;">
        <b>Index:</b> {block["index"]}<br>
        <b>File:</b> {block["file_name"]}<br>
        <b>Owner:</b> {block["owner"]}<br>
        <b>Receiver:</b> {block["receiver"]}<br>
        <b>Hash:</b> {block["hash"][:16]}
        </div>
        """

    return html