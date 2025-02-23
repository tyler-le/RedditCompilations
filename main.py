import argparse
from src.controller.download_controller import download_controller
from src.controller.merge_controller import merge_controller
from src.controller.upload_controller import upload_controller
from src.managers.config_manager import ConfigManager

if __name__ == "__main__":
    # Step 1: Get arguments passed in command line
    parser = argparse.ArgumentParser(description="Download videos from a subreddit and upload to YouTube.")
    parser.add_argument("subreddit_name", help="Name of the subreddit to fetch videos from")
    args = parser.parse_args()    
    subreddit_name = args.subreddit_name
    
    # Step 2: Fetch subreddit details from the config (title, description, etc.)
    subreddit_details = ConfigManager.get_video_details(subreddit_name)

    # Step 3: Call fetch_top_videos from RedditWrapper to download the videos
    download_folder = download_controller(subreddit_name, subreddit_details['duration_in_seconds'])
    
    # Step 4: Stitch and re-encode downloaded videos
    output_path = merge_controller(download_folder)
    
    # Step 5: Upload video to YouTube
    # video_link = upload_controller(output_path, title, description, category, privacy, upload_date)
    video_link = upload_controller(output_path, subreddit_details)

    print(f"✅ Video uploaded to {video_link}")
