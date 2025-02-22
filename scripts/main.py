from download_from_reddit import fetch_top_videos
from merge_videos import stitch_videos_in_folder
from upload_to_youtube import upload_video_from_path

if __name__ == "__main__":
    # Step 1: Fetch and download videos
    download_folder = fetch_top_videos()

    # Step 2: Stitch and re-encode downloaded videos
    output_path = stitch_videos_in_folder(download_folder)
    
    # Step 3: Upload video to YouTube
    # video_link = upload_video_from_path(output_path, "Title", "Description", "20", "private")
    
    # print(f"✅ Video uploaded to {video_link}")
