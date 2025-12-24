from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import instaloader
import os
import shutil
import tempfile

app = FastAPI()

# Configura CORS para Lovable
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode colocar o domínio do Lovable
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

L = instaloader.Instaloader()

@app.get("/")
def read_root():
    return {"status": "API funcionando"}

@app.get("/download")
def download_post(url: str = Query(..., description="URL do post do Instagram")):
    temp_dir = tempfile.mkdtemp()
    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_s_
