import json
from src.constants.constants import BATCH_UPLOAD_PATH, CREATE_CONFIG_CHOICE, DURATION_IN_SECONDS_KEY, LOAD_CONFIG_CHOICE, OUTPUT_PATH_KEY, UPLOAD_DETAILS_KEY
from src.controller.download_controller import download_controller
from src.controller.merge_controller import merge_controller
from src.util.config_util import ConfigUtil

if __name__ == "__main__":  
    # Step 1: Ask user whether to load the config or create a new one
    config_choice = ConfigUtil.get_user_config_choice()
    
    if config_choice == LOAD_CONFIG_CHOICE:
        # Load the subreddit configs from file
        config_path = ConfigUtil.prompt_choose_config()
        subreddit_details = ConfigUtil.load_subreddit_config(config_path)
    elif config_choice == CREATE_CONFIG_CHOICE:
        # Allow the user to define their own configuration (you can add more logic for this)
        print("Creating a new configuration.")
        subreddit_details = ConfigUtil.prompt_custom_config()  
    else:
        # If user chooses 'n', just proceed without loading the config
        print("Skipping config loading.")
        subreddit_details = {}

    batch_uploads = []

    for subreddit_name, upload_details in subreddit_details.items():
        try:
            # Step 2: Call fetch_top_videos from RedditWrapper to download the videos
            download_folder = download_controller(subreddit_name, upload_details[DURATION_IN_SECONDS_KEY])
            
            # Step 3: Stitch and re-encode downloaded videos
            output_path = merge_controller(download_folder)
            
            # Step 4: Add to batch
            batch_uploads.append({OUTPUT_PATH_KEY: output_path, UPLOAD_DETAILS_KEY: upload_details})
            
            # Step 5: Increment episode for next time
            ConfigUtil.increment_episode(subreddit_name)

        except Exception as e:
            print(f"Error processing {subreddit_name}: {e}")

    # Step 5: Write the batch upload details to a file
    with open(BATCH_UPLOAD_PATH, "w") as f:
        json.dump(batch_uploads, f)
