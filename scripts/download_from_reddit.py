import os
import json
import time
import yt_dlp
import praw
from datetime import datetime
from slugify import slugify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch Reddit API credentials from environment variables
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "my_bot/1.0")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing Reddit API credentials. Set them in the .env file.")

# Configuration
SUBREDDIT = "FunnyAnimals"
MAX_DURATION = 750
MAX_RETRIES = 3

# Initialize Reddit API
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

def get_video_duration(url):
    """Retrieve video duration using yt-dlp (returns duration in seconds)."""
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "force_generic_extractor": False
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("duration", 0)
    except Exception as e:
        print(f"⚠️ Failed to get duration for {url}: {e}")
        return 0

def save_metadata(folder, filename, title):
    """Save video metadata (original title) in a JSON file."""
    metadata_path = os.path.join(folder, "metadata.json")

    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    metadata[filename] = title

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

def download_video(url, folder, title):
    """Download MP4 video with audio using yt-dlp."""
    sanitized_title = slugify(title)
    filename = f"{sanitized_title}.mp4"
    output_path = os.path.join(folder, filename)

    ydl_opts = {
        "outtmpl": output_path,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "merge_output_format": "mp4",
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "quiet": False
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"✅ Downloaded: {url}")
            save_metadata(folder, filename, title)
            return True
        except Exception as e:
            print(f"❌ Attempt {attempt} failed for {url} | Error: {e}")
            time.sleep(3)

    print(f"⏹️ Skipping {url} after {MAX_RETRIES} failed attempts.")
    return False

def fetch_top_videos():
    """Fetch and download videos while respecting Reddit's API limits."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    download_folder = os.path.join("downloaded_videos", timestamp)
    os.makedirs(download_folder, exist_ok=True)

    subreddit = reddit.subreddit(SUBREDDIT)
    total_duration = 0
    downloaded_count = 0

    for post in subreddit.top(time_filter="week"):
        if not post.is_video:
            continue
        print(f"🎬 Found video: {post.title}")

        duration = get_video_duration(post.url)
        if duration == 0 or duration > 45:
            print(f"⚠️ Skipping {post.url} (duration unknown or too long)")
            continue

        if total_duration + duration > MAX_DURATION:
            print(f"⏹️ Stopping downloads: Reached {total_duration / 60:.2f} min of videos")
            break

        download_video(post.url, download_folder, post.title)
        total_duration += duration
        downloaded_count += 1

    print(f"✅ Total videos downloaded: {downloaded_count} ({total_duration / 60:.2f} min)")
    print(f"📂 Videos saved in: {download_folder}")
    return download_folder

if __name__ == "__main__":
    fetch_top_videos()
