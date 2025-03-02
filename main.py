import json
from src.constants.constants import BATCH_UPLOAD_PATH, CONFIG_PATH_KEY, DURATION_IN_SECONDS_KEY, OUTPUT_PATH_KEY, SUBREDDIT_NAME_KEY, UPLOAD_DETAILS_KEY
from src.controller.download_controller import download_controller
from src.controller.merge_controller import merge_controller
from src.util.config_util import ConfigUtil

if __name__ == "__main__":  
    # Step 1: Ask user to load a config
    config_service = ConfigUtil()
    config_path = config_service.prompt_choose_config()
    subreddit_details = config_service.load_subreddit_config(config_path) 

    batch_uploads = []
    for subreddit_name, upload_details in subreddit_details.items():
        try:
            # Step 2: Call fetch_top_videos from RedditWrapper to download the videos
            download_folder = download_controller(subreddit_name, upload_details[DURATION_IN_SECONDS_KEY])
            
            # Step 3: Stitch and re-encode downloaded videos
            output_path = merge_controller(download_folder)
            
            # Step 4: Add to batch
            batch_uploads.append({SUBREDDIT_NAME_KEY: subreddit_name, OUTPUT_PATH_KEY: output_path, UPLOAD_DETAILS_KEY: upload_details, CONFIG_PATH_KEY: config_path})

        except Exception as e:
            print(f"Error processing {subreddit_name}: {e}")

    # Step 5: Write the batch upload details to a file
    with open(BATCH_UPLOAD_PATH, "w") as f:
        json.dump(batch_uploads, f)
