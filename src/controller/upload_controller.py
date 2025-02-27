import sys
from src.handler.upload_handler import upload_video

def upload_controller(file_path, upload_details, youtube_credentials):
    """Controller function to upload a video."""
    if not file_path or not upload_details:
        print("Error: Missing required parameters")
        sys.exit(1)

    return upload_video(youtube_credentials, file_path, upload_details)