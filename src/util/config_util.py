import json
import os
from src.constants.constants import CREATE_CONFIG_CHOICE, LOAD_CONFIG_CHOICE

class ConfigUtil:
    # config_path = "src/configs/subreddit_config.json"
    config_path = "src/configs/gaming_config.json"

    @staticmethod
    def load_subreddit_config(path=config_path):
        """Load the subreddit configuration from the JSON file."""
        with open(path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_subreddit_config(config):
        """Save the updated subreddit configuration back to the JSON file."""
        with open(ConfigUtil.config_path, 'w') as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def increment_episode(subreddit_name):
        """Increment the episode and update the title in the config."""
        config = ConfigUtil.load_subreddit_config()
        
        if subreddit_name not in config:
            raise ValueError(f"Configuration for subreddit '{subreddit_name}' not found.")
        
        # Get the current episode and increment it by 1
        current_episode = config[subreddit_name]["episode"]
        new_episode = current_episode + 1
        
        # Update the episode in the config
        config[subreddit_name]["episode"] = new_episode
        
        # Save the updated config back to the file
        ConfigUtil.save_subreddit_config(config)
        
        # Return the incremented episode number
        return new_episode

    @staticmethod
    def save_metadata(folder, filename, title):
        """Save video metadata (original title) in a JSON file."""
        metadata_path = os.path.join(folder, "metadata.json")

        # Load existing metadata if it exists
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
        else:
            metadata = {}

        # Add the new metadata entry
        metadata[filename] = title

        # Save the updated metadata back to the JSON file
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
    @staticmethod
    def get_user_config_choice():
        while True:
            user_choice = input("Do you want to load the config from file (1) or create your own (2)? ").strip()
            if user_choice in [LOAD_CONFIG_CHOICE, CREATE_CONFIG_CHOICE]:
                return user_choice
            else:
                print("Invalid choice, please enter '1' to load or '2' to create your own.")

    @staticmethod
    def prompt_custom_config():
        subreddit_name = input(f"Enter the subreddit name: ").strip()
        title = input(f"Enter title for the video: ").strip()
        description = input(f"Enter description for the video: ").strip()
        category = input(f"Enter category for the video (e.g., 23): ").strip()
        privacy = input(f"Enter privacy for the video (e.g., private): ").strip()
        episode = int(input(f"Enter episode number for the video: ").strip())
        duration_in_seconds = int(input(f"Enter duration in seconds for the video (e.g., 600): ").strip())
        publish_day = input(f"Enter publish day for the video (e.g., Monday): ").strip()

        # Returning the config in the format required
        return {
            subreddit_name: {
                "title": title,
                "description": description,
                "category": category,
                "privacy": privacy,
                "episode": episode,
                "duration_in_seconds": duration_in_seconds,
                "publish_day": publish_day
            }
        }
            
