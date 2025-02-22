import argparse
from scripts.download_from_reddit import fetch_top_videos
from scripts.merge_videos import stitch_videos_in_folder
from scripts.upload_to_youtube import upload_video_from_path
from managers.config_manager import ConfigManager

if __name__ == "__main__":
    # Set up argparse to accept the subreddit name as an argument
    parser = argparse.ArgumentParser(description="Download videos from a subreddit and upload to YouTube.")
    parser.add_argument("subreddit_name", help="Name of the subreddit to fetch videos from")
    args = parser.parse_args()
    
    # Use the provided subreddit name
    subreddit_name = args.subreddit_name
    
    # Step 2: Fetch subreddit details from the config (title, description, etc.)
    title, description, category, privacy, episode, duration_in_seconds = ConfigManager.get_subreddit_details(subreddit_name)
    
    # Step 3: Call fetch_top_videos from RedditWrapper to download the videos
    download_folder = fetch_top_videos(subreddit_name, duration_in_seconds)
    
    # Step 4: Stitch and re-encode downloaded videos
    output_path = stitch_videos_in_folder(download_folder)
    
    # Step 5: Upload video to YouTube
    # video_link = upload_video_from_path(output_path, title, description, category, privacy)
    
    # print(f"✅ Video uploaded to {video_link}")
