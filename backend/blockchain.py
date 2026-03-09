import hashlib
import json
import time
import os

BLOCKCHAIN_FILE = "storage/blockchain.json"


class Blockchain:

    def __init__(self):

        self.chain = []

        if os.path.exists(BLOCKCHAIN_FILE):

            with open(BLOCKCHAIN_FILE,"r") as f:
                self.chain = json.load(f)

        else:

            self.create_genesis()

    # ==========================================
    # Genesis Block
    # ==========================================

    def create_genesis(self):

        block = {
            "index":0,
            "timestamp":time.time(),
            "file_name":"genesis",
            "encrypted_key":"none",
            "owner":"system",
            "receiver":"none",
            "permissions":["system"],
            "prev_hash":"0"
        }

        block["hash"] = self.hash(block)

        self.chain.append(block)

        self.save()

    # ==========================================

    def hash(self,block):

        return hashlib.sha256(
            json.dumps(block,sort_keys=True).encode()
        ).hexdigest()

    # ==========================================
    # Add Block
    # ==========================================

    def add_block(self,file_name,key,owner,receiver):

        prev = self.chain[-1]

        block = {

            "index":len(self.chain),

            "timestamp":time.time(),

            "file_name":file_name,

            "encrypted_key":key.hex(),

            "owner":owner,

            "receiver":receiver,

            "permissions":[owner,receiver],

            "prev_hash":prev["hash"]
        }

        block["hash"] = self.hash(block)

        self.chain.append(block)

        self.save()

    # ==========================================

    def save(self):

        os.makedirs("storage",exist_ok=True)

        with open(BLOCKCHAIN_FILE,"w") as f:

            json.dump(self.chain,f,indent=4)