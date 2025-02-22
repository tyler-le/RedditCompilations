import os
import praw
import yt_dlp
import time
from dotenv import load_dotenv
from managers.config_manager import ConfigManager


class RedditWrapper:
    def __init__(self):
        """Initialize Reddit API client and load environment variables."""
        # Load environment variables from .env file
        load_dotenv()

        # Fetch Reddit API credentials from environment variables
        self.CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
        self.USER_AGENT = os.getenv("REDDIT_USER_AGENT", "my_bot/1.0")

        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise ValueError("Missing Reddit API credentials. Set them in the .env file.")

        # Initialize Reddit API client
        self.reddit = praw.Reddit(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            user_agent=self.USER_AGENT
        )
        
        self.MAX_RETRIES = 3

    def get_video_duration(self, url):
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

    def fetch_top_videos(self, subreddit_name: str, duration_in_seconds: int):
        """Fetch and download videos while respecting Reddit's API limits."""
        # Create folder for saving the downloaded videos
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        download_folder = f"/Users/tylerle/Desktop/yt-reddit-scraper/output/{timestamp}"

        # Initialize total video duration and downloaded count
        total_duration = 0
        downloaded_count = 0

        subreddit = self.reddit.subreddit(subreddit_name)

        for post in subreddit.top(time_filter="week"):
            if not post.is_video:
                continue
            print(f"🎬 Found video: {post.title}")

            duration = self.get_video_duration(post.url)
            if duration == 0 or duration > 45:
                print(f"⚠️ Skipping {post.url} (duration unknown or too long)")
                continue
            
            if total_duration + duration > duration_in_seconds:
                print(f"⏹️ Stopping downloads: Reached {total_duration / 60:.2f} min of videos")
                break

            self.download_video(post.url, download_folder, post.title, self.MAX_RETRIES)
            total_duration += duration
            downloaded_count += 1

        print(f"✅ Total videos downloaded: {downloaded_count} ({total_duration / 60:.2f} min)")
        print(f"📂 Videos saved in: {download_folder}")
        return download_folder

    def download_video(self, url, folder, title, max_retries):
        """Download MP4 video with audio using yt-dlp."""
        sanitized_title = title.replace(" ", "_")  # Using basic string replace for simplicity
        filename = f"{sanitized_title}.mp4"
        output_path = f"{folder}/{filename}"

        ydl_opts = {
            "outtmpl": output_path,
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "merge_output_format": "mp4",
            "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            "quiet": False
        }

        for attempt in range(1, max_retries + 1):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print(f"✅ Downloaded: {url}")
                ConfigManager.save_metadata(folder, filename, title)
                return True
            except Exception as e:
                print(f"❌ Attempt {attempt} failed for {url} | Error: {e}")
                time.sleep(3)

        print(f"⏹️ Skipping {url} after {max_retries} failed attempts.")
        return False


