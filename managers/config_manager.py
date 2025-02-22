import json
import os

class ConfigManager:
    config_path = "/Users/tylerle/Desktop/yt-reddit-scraper/configs/subreddit_config.json"

    @staticmethod
    def load_subreddit_config():
        """Load the subreddit configuration from the JSON file."""
        with open(ConfigManager.config_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_subreddit_config(config):
        """Save the updated subreddit configuration back to the JSON file."""
        with open(ConfigManager.config_path, 'w') as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def increment_episode(subreddit_name):
        """Increment the episode and update the title in the config."""
        config = ConfigManager.load_subreddit_config()
        
        if subreddit_name not in config:
            raise ValueError(f"Configuration for subreddit '{subreddit_name}' not found.")
        
        # Get the current episode and increment it by 1
        current_episode = config[subreddit_name]["episode"]
        new_episode = current_episode + 1
                
        # Update the episode in the config
        config[subreddit_name]["episode"] = new_episode
        
        # Save the updated config back to the file
        ConfigManager.save_subreddit_config(config)
        
        # Return the incremented episode number
        return new_episode
    
    @staticmethod
    def get_subreddit_details(subreddit_name):
        """Get the details for a specific subreddit from the config."""
        config = ConfigManager.load_subreddit_config()
        
        if subreddit_name not in config:
            raise ValueError(f"Configuration for subreddit '{subreddit_name}' not found.")
        
        subreddit_config = config[subreddit_name]

        # Get the incremented episode number
        episode = ConfigManager.increment_episode(subreddit_name) - 1
        
        # Generate title with episode
        title = f"{subreddit_config.get('title')}{episode}"
        description = subreddit_config.get("description")
        category = subreddit_config.get("category")
        privacy = subreddit_config.get("privacy", "private")  
        duration_in_seconds = subreddit_config.get("duration_in_seconds", 780)  # default to 780s (13 minutes)

        # Return the values
        return title, description, category, privacy, episode, duration_in_seconds

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
