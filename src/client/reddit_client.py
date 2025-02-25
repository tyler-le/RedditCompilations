import os
from src.constants.constants import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
import praw
import time
from dotenv import load_dotenv
from src.util.config_util import ConfigUtil
import subprocess
class RedditWrapper:
    def __init__(self):
        """Initialize Reddit API client and load environment variables."""
        # Load environment variables from .env file
        load_dotenv()

        # Fetch Reddit API credentials from environment variables
        self.CLIENT_ID = os.getenv(REDDIT_CLIENT_ID)
        self.CLIENT_SECRET = os.getenv(REDDIT_CLIENT_SECRET)
        self.USER_AGENT = os.getenv(REDDIT_USER_AGENT, "my_bot/1.0")

        if not self.CLIENT_ID or not self.CLIENT_SECRET:
            raise ValueError("Missing Reddit API credentials. Set them in the .env file.")

        # Initialize Reddit API client
        self.reddit = praw.Reddit(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            user_agent=self.USER_AGENT
        )
        
    def get_video_duration(self, url):
        """Retrieve video duration using yt-dlp (returns duration in seconds)."""
        cookies_path = os.path.expanduser("~/yt-reddit-scraper/cookies.txt")  # Expanding the ~ to full path
        command = ['yt-dlp', '--cookies', cookies_path, '--get-duration', url]
        
        try:
            # Run the command and capture the output
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return int(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to get duration for {url}: {e}")
            return 0

    def fetch_top_videos(self, subreddit_name: str, duration_in_seconds: int):
        """Fetch and download videos while respecting Reddit's API limits."""
        # Create folder for saving the downloaded videos
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        download_folder = os.path.join("output", subreddit_name, timestamp)
        
        # Initialize total video duration and downloaded count
        total_duration = 0
        downloaded_count = 0

        subreddit = self.reddit.subreddit(subreddit_name)

        for post in subreddit.top(time_filter="week"):
            if not post.is_video:
                continue
            print(f"🎬 Found video: {post.title}")

            duration = self.get_video_duration(post.url)
            if duration == 0 or duration > 30:
                print(f"⚠️ Skipping {post.url} (duration unknown or too long)")
                continue
            
            if total_duration + duration > duration_in_seconds:
                print(f"⏹️ Stopping downloads: Reached {total_duration / 60:.2f} min of videos")
                break

            if self.download_video(post.url, download_folder, post.title, downloaded_count):
                print(f"Downloaded video #{downloaded_count} - {post.title} with a duration of {duration}")
                total_duration += duration
                downloaded_count += 1
                print(f"🕦 Current total duration (in seconds): {total_duration}")
            else:
                print(f"Unable to download video {post.title} with a duration of {duration}")

            time.sleep(2)
            

        print(f"✅ Total videos downloaded: {downloaded_count} ({total_duration / 60:.2f} min)")
        print(f"📂 Videos saved in: {download_folder}")
        return download_folder

    def download_video(self, url, folder, title, download_count):
        """Download MP4 video with audio using yt-dlp."""
        filename = f"{download_count}.mp4"
        output_path = f"{folder}/{filename}"

        cookies_path = os.path.expanduser("~/yt-reddit-scraper/cookies.txt")  # Expanding the ~ to full path
        command = [
            'yt-dlp',
            '--cookies', cookies_path,
            '--output', output_path,
            '--quiet',
            '--retries', '10',
            url
        ]
        
        try:
            # Run the command to download the video
            subprocess.run(command, check=True)
            print(f"✅ Downloaded: {url}")
            ConfigUtil.save_metadata(folder, filename, title)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Download failed for {url} | Error: {e}")
            return False

