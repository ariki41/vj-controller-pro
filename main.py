import os
import shutil
import uvicorn
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

OS_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.normpath(os.path.join(OS_DIR, "videos"))
PUBLIC_DIR = os.path.normpath(os.path.join(OS_DIR, "public"))

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)

app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")
app.mount("/static", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")

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
        'nocheckcertificate': True,
        'rm_cache_dir': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
    print("\n" + "="*60)
    print("VJ Controller Pro 起動準備完了")
    print(f"プレーヤーURL➡ http://localhost:8000/static/control.html")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)