import json
import os
from src.util.upload_scheduler_util import UploadSchedulerUtil

class ConfigUtil:
    config_path = "src/configs/subreddit_config.json"

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
