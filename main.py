from fastapi import FastAPI, HTTPException
import instaloader
import os
import shutil
import zipfile
from uuid import uuid4

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/download")
def download(username: str):
    try:
        # pasta temporária única
        session_id = str(uuid4())
        base_path = f"/tmp/{session_id}"
        os.makedirs(base_path, exist_ok=True)

        L = instaloader.Instaloader(
            download_video_thumbnails=False,
            download_geotags=False,
            save_metadata=False,
            dirname_pattern=base_path,
            filename_pattern="{shortcode}"
        )

        L.download_profile(username, profile_pic=False)

        zip_path = f"/tmp/{username}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for foldername, _, filenames in os.walk(base_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zipf.write(file_path, arcname=filename)

        shutil.rmtree(base_path)

        return {
            "message": "Download concluído",
            "file": zip_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
