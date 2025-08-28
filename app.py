from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Video Downloader API is running"}

@app.get("/download")
def download_video(url: str = Query(..., description="Video URL")):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return JSONResponse({
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "formats": info.get("formats"),
                "download_url": info.get("url")  # direct playable URL
            })

    except Exception as e:
        return {"error": str(e)}
