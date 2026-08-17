import os
import shutil
import sys
import uvicorn
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp

RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
APPLICATION_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else RESOURCE_DIR
)

VERSION_FILE = os.path.join(RESOURCE_DIR, "VERSION")
with open(VERSION_FILE, encoding="utf-8") as version_file:
    APP_VERSION = version_file.read().strip()

app = FastAPI(title="VJ Controller Pro", version=APP_VERSION)

VIDEO_DIR = os.path.join(APPLICATION_DIR, "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)

app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(RESOURCE_DIR, "public"), html=True),
    name="public",
)

dl_status = {"current": None}

class DownloadRequest(BaseModel):
    url: str

def my_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0.0%').strip()
        dl_status['current'] = f"DL中: {percent}"
    elif d['status'] == 'finished':
        dl_status['current'] = "処理中..."

def download_video(url: str):
    dl_status['current'] = "開始..."
    ydl_opts = {
        'outtmpl': os.path.join(VIDEO_DIR, '%(title)s.%(ext)s'),
        'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
        'windowsfilenames': True,
        'noplaylist': True,
        'quiet': True,
        'progress_hooks': [my_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Download Error: {e}")
    finally:
        dl_status['current'] = None

@app.post("/api/download")
async def download(req: DownloadRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(download_video, req.url)
    return {"status": "downloading_started"}

@app.get("/api/progress")
async def get_progress():
    return {"progress": dl_status.get('current')}

@app.get("/api/videos")
async def get_videos():
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.webm', '.mov', '.m4v', '.gif', '.png', '.jpg', '.jpeg', '.webp'))]
    return {"videos": files}

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(VIDEO_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "filename": file.filename}

if __name__ == "__main__":
    if "--version" in sys.argv:
        print(APP_VERSION)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
