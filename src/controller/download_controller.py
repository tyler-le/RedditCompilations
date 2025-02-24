from src.handler.download_handler import fetch_top_videos

def download_controller(subreddit_name, duration_in_seconds):
    if not subreddit_name or not duration_in_seconds:
        raise ValueError("Missing required parameters")
    
    print(f"👀 Fetching videos for subreddit r/{subreddit_name}")
    return fetch_top_videos(subreddit_name, duration_in_seconds)

if __name__ == "__main__":
    subreddit_name = input("Enter subreddit name: ")
    duration_in_seconds = int(input("Enter duration in seconds: "))
    try:
        download_folder = download_controller(subreddit_name, duration_in_seconds)
        print(f"✅ Total videos downloaded and saved in {download_folder}")
    except ValueError as e:
        print(f"Error: {e}")
