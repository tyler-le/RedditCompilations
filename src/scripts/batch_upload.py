import json
import sys
from concurrent.futures import ThreadPoolExecutor

from ..handler.upload_handler import authenticate_youtube
from src.util.upload_scheduler_util import UploadSchedulerUtil
from ..constants.constants import BATCH_UPLOAD_PATH, OUTPUT_PATH_KEY, UPLOAD_DETAILS_KEY
from src.controller.upload_controller import upload_controller


def load_batch_from_json(filename=BATCH_UPLOAD_PATH):
    """Load batch upload details from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filename}.")
        sys.exit(1)

    """
    Call this script like `python3 -m src.scripts.batch_upload`
    It will look for a json file at output/batch_upload.json
    Using that config, it will upload each video concurrently
    """
if __name__ == "__main__":
    batch_upload = load_batch_from_json()

    if not batch_upload:
        print("No videos to upload.")
        sys.exit(0)

    youtube_credentials = authenticate_youtube() 

    for item in batch_upload:
        upload_controller(item[OUTPUT_PATH_KEY], item[UPLOAD_DETAILS_KEY], youtube_credentials)
            