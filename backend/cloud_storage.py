import os
from supabase import create_client

# ===============================
# Supabase Config
# ===============================

SUPABASE_URL = "https://qodnhmonppsxzsjrmxpq.supabase.co"
SUPABASE_KEY = "sb_publishable_nS0v-R9NJOAre49USqfyFw_mwV8Rare"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "secure-files"


# ===============================
# Upload File
# ===============================

def upload_file(file_path):

    try:

        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            file_data = f.read()

        result = supabase.storage.from_(BUCKET).upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": "application/octet-stream"}
        )

        print("Supabase upload result:", result)

        return file_name

    except Exception as e:

        print("Supabase upload error:", e)

        return None


# ===============================
# Download File
# ===============================

def download_file(file_name):

    try:

        data = supabase.storage.from_(BUCKET).download(file_name)

        os.makedirs("storage", exist_ok=True)

        path = f"storage/{file_name}"

        with open(path, "wb") as f:
            f.write(data)

        return path

    except Exception as e:

        print("Supabase download error:", e)

        return None