from src.client.reddit_client import RedditWrapper

# Initialize RedditWrapper
reddit_wrapper = RedditWrapper()

def fetch_top_videos(subreddit_name, duration_in_seconds):
    """Fetch and download videos while respecting Reddit's API limits."""
    download_folder = reddit_wrapper.fetch_top_videos(subreddit_name, duration_in_seconds)
    print(f"✅ Total videos downloaded and saved in {download_folder}")
    return download_folder
