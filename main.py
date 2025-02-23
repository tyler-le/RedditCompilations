import argparse
from concurrent.futures import ThreadPoolExecutor
from src.controller.download_controller import download_controller
from src.controller.merge_controller import merge_controller
from src.controller.upload_controller import upload_controller
from src.managers.config_manager import ConfigManager

if __name__ == "__main__":
    # Step 1: Get arguments passed in command line
    parser = argparse.ArgumentParser(description="Download videos from subreddits and upload to YouTube.")
    parser.add_argument("subreddit_names", nargs='+', help="List of subreddits to fetch videos from")
    args = parser.parse_args()    
    subreddit_names = args.subreddit_names
    
    batch_upload = []
    for subreddit_name in subreddit_names:
        # Step 2: Fetch subreddit details from the config (title, description, etc.)
        upload_details = ConfigManager.get_video_details(subreddit_name)

        # Step 3: Call fetch_top_videos from RedditWrapper to download the videos
        download_folder = download_controller(subreddit_name, upload_details['duration_in_seconds'])
        
        # Step 4: Stitch and re-encode downloaded videos
        output_path = merge_controller(download_folder)
        
        # Step 5: Add to batch
        batch_upload.append([output_path, upload_details])
    
    # Step 6: Batch upload the videos
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your system's capacity
        futures = []
        for path, video_details in batch_upload:
            future = executor.submit(upload_controller, path, video_details)
            futures.append(future)   

        # Wait for all tasks to complete
        for future in futures:
            future.result()
