from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
import requests
import os
import uuid
import shutil

from auth import verify_credentials
from reddit_client import RedditPoster

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reddit API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
USER_AGENT = os.getenv("USER_AGENT")

poster = RedditPoster(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    refresh_token=REFRESH_TOKEN,
    user_agent=USER_AGENT
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class MediaRequest(BaseModel):
    oauth_token: str
    subreddit: str
    title: str
    body_text: str = ""
    media_url: str

def download_file_from_url(media_url: str) -> str:
    filename = f"{uuid.uuid4()}.media"
    path = os.path.join(UPLOAD_DIR, filename)

    r = requests.get(media_url, stream=True)
    if r.status_code != 200:
        raise Exception("Failed to download media from URL.")
    
    with open(path, "wb") as f:
        shutil.copyfileobj(r.raw, f)

    return path

@app.post("/publishImage")
async def publish_image(data: MediaRequest, username: str = Depends(verify_credentials)):
    try:
        media_path = download_file_from_url(data.media_url)
        post_url = await run_in_threadpool(poster.post_image, data.subreddit, data.title, media_path)
        return {"status": "success", "url": post_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/publishVideo")
async def publish_video(data: MediaRequest, username: str = Depends(verify_credentials)):
    try:
        media_path = download_file_from_url(data.media_url)
        post_url = await run_in_threadpool(poster.post_video, data.subreddit, data.title, media_path)
        return {"status": "success", "url": post_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}