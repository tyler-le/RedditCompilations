from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

# OAuth 2.0 Scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube():
    """Authenticate the user and build the YouTube API client."""
    print("Current working directory:", os.getcwd())

    # Use a fixed port (8080) to avoid dynamic redirect URI
    flow = InstalledAppFlow.from_client_secrets_file('src/configs/config.json', SCOPES)
    
    # Here, we are fixing the redirect URI with a specific port (8080)
    credentials = flow.run_local_server(port=8080)  # Use port 8080 for fixed redirect URI
    
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

def upload_video(youtube, file_path, subreddit_details):
    """Upload a video to YouTube."""
    print(f"👀 Attempting to upload video at {file_path} to YouTube")
    title, description, category, privacy, episode, duration_in_seconds, upload_date = subreddit_details.values()
    
    try:
        # Validate the category to ensure it is a valid YouTube category ID
        category_id = str(category)  # Ensure category is a string of a valid YouTube category ID
        
        # Call the API's videos.insert method to upload the video
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "videoCategoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy,  
                    "publishAt": upload_date
                }
            },
            media_body=file_path
        )
        response = request.execute()

        print(f"Video '{title}' was successfully uploaded.")
        print(f"Video URL: https://www.youtube.com/watch?v={response['id']}")
        return f"https://www.youtube.com/watch?v={response['id']}"

    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def upload_video_from_path(file_path, subreddit_details):
    """Authenticate and upload a video using the file path."""
    youtube = authenticate_youtube() 
    return upload_video(youtube, file_path, subreddit_details)
