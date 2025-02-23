import sys
from src.handler.upload_handler import upload_video_from_path

def upload_controller(file_path, subreddit_details):
    """Controller function to upload a video."""
    if not file_path or not subreddit_details:
        print("Error: Missing required parameters")
        sys.exit(1)

    return upload_video_from_path(file_path, subreddit_details)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <file_path> <title> <description> <category> <privacy_status>")
        sys.exit(1)

    file_path = sys.argv[1]
    title = sys.argv[2]
    description = sys.argv[3]
    category = sys.argv[4]  # Ensure this is a valid YouTube category ID
    privacy_status = sys.argv[5]  # 'public', 'private', or 'unlisted'
    upload_date = sys.argv[6]

    # Call the controller to upload the video
    upload_controller(file_path, title, description, category, privacy_status, upload_date)
