import json
import os
from src.constants.constants import CREATE_CONFIG_CHOICE, LOAD_CONFIG_CHOICE, CONFIG_DIR

class ConfigUtil:
    _instance = None  # Class variable to hold the instance

    def __new__(cls, config_path="src/configs/subreddit_config.json"):
        """Override the __new__ method to implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ConfigUtil, cls).__new__(cls)
            cls._instance.config_path = config_path
        return cls._instance

    def load_subreddit_config(self, config_path):
        """Load the subreddit configuration from the JSON file."""
        with open(config_path, 'r') as f:
            return json.load(f)

    def save_subreddit_config(self, config, config_path):
        """Save the updated subreddit configuration back to the JSON file."""
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

    def increment_episode(self, subreddit_name, config_path):
        """Increment the episode and update the title in the config."""
        config = self.load_subreddit_config(config_path)
        print(subreddit_name, config)
        if subreddit_name not in config:
            raise ValueError(f"Configuration for subreddit '{subreddit_name}' not found.")
        
        # Get the current episode and increment it by 1
        current_episode = config[subreddit_name]["episode"]
        new_episode = current_episode + 1
        
        # Update the episode in the config
        config[subreddit_name]["episode"] = new_episode
        
        # Save the updated config back to the file
        self.save_subreddit_config(config, config_path)
        
        # Return the incremented episode number
        return new_episode

    def save_metadata(self, folder, filename, title):
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
            
    def prompt_choose_config(self):
        # List all files in the config directory
        try:
            config_files = [f for f in os.listdir(CONFIG_DIR) if os.path.isfile(os.path.join(CONFIG_DIR, f))]
            
            if not config_files:
                print("No configuration files found.")
                return None
            
            # Display the files with a prompt to choose one
            print("Available configuration files:")
            for idx, file in enumerate(config_files, start=1):
                print(f"{idx}. {file}")

            # Ask the user to choose a config file
            choice = input(f"Choose a configuration file (1-{len(config_files)}): ")

            # Validate the input and return the chosen config file
            try:
                choice = int(choice)
                if 1 <= choice <= len(config_files):
                    ret = os.path.join(CONFIG_DIR, config_files[choice - 1])  # Set the global variable
                    self.config_path = os.path.join(CONFIG_DIR, config_files[choice - 1])
                    return self.config_path
                else:
                    print("Invalid choice, please select a valid number.")
                    return None
            except ValueError:
                print("Invalid input, please enter a number.")
                return None
        except FileNotFoundError:
            print(f"The directory '{CONFIG_DIR}' does not exist.")
            return None
