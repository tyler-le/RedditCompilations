import os
import json
import subprocess
import concurrent.futures
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip
from src.client.s3_client import S3Client
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
# Configuration
ENCODED_RESOLUTION = "1280x720"
FRAME_RATE = 30
THREADS = 4 

aws_client = S3Client()

def check_video_format(input_path):
    """Check if the video format, resolution, and frame rate match the required settings."""
    print(f"Checking video format for {input_path}...")
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate", "-of", "csv=p=0", input_path
    ]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode("utf-8").strip().split("\n")
        width, height = map(int, output[0].split(",")[:2])  # Extract width and height
        frame_rate = round(eval(output[0].split(",")[2]))  # Convert frame rate to integer

        if (width, height) == (1280, 720) and frame_rate == FRAME_RATE:
            print(f"✅ {input_path} is already in the correct format.")
            return True
        else:
            print(f"⚠️ {input_path} does not match required format.")
            return False
    except Exception as e:
        print(f"⚠️ Failed to check format for {input_path}: {e}")
        return False


def reencode_video(input_path, output_path):
    """Re-encode video to ensure uniform format with black bars if needed."""
    print(f"Re-encoding {input_path}...")
    command = [
        "ffmpeg", "-i", input_path,
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
        "-preset", "fast", "-r", str(FRAME_RATE), "-s", ENCODED_RESOLUTION,
        "-vf", "scale=-1:720,pad=1280:720:(ow-iw)/2:(oh-ih)/2",  # Add black bars
        "-strict", "experimental", output_path, "-y"
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {input_path} re-encoded successfully.")
        return output_path
    except Exception as e:
        print(f"❌ Error re-encoding {input_path}: {e}")
        return None


def reencode_video_concurrent(input_path, output_folder):
    """Helper function to handle re-encoding in parallel."""
    reencoded_path = os.path.join(output_folder, f"reencoded_{os.path.basename(input_path)}")
    return reencode_video(input_path, reencoded_path)


def add_text_overlay(video_clip, text):
    """Adds text overlay with a black semi-transparent background."""
    print("Adding text overlay to video...")

    width, height = video_clip.size
    position = ("center", height * 0.85)  # Slightly above the bottom for horizontal videos

    # Create text clip
    txt_clip = TextClip(
    text,
    fontsize=36,
    color='white',
    font="Arial-Bold",
    stroke_color="black",
    stroke_width=2,
    method="caption",
    size=(width * 0.9, None)  # Set the width of the text to 90% of video width, height is auto
).set_duration(video_clip.duration)

    # Create a black background rectangle slightly larger than the text
    padding = 10  # Padding around text
    bg_width, bg_height = txt_clip.size[0] + 2 * padding, txt_clip.size[1] + 2 * padding

    bg_clip = ColorClip(size=(bg_width, bg_height), color=(0, 0, 0)) \
        .set_opacity(0.6) \
        .set_duration(video_clip.duration)

    # Position both the background and text
    txt_clip = txt_clip.set_position(position)
    bg_clip = bg_clip.set_position(position)

    return CompositeVideoClip([video_clip, bg_clip, txt_clip])


def stitch_videos_in_folder(folder_path):
    """Stitches all videos in the folder into a single output video with text overlays."""
    print(f"Stitching videos from folder: {folder_path}...")
    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4'))]
    if not video_files:
        print("⚠️ No video files found.")
        return None

    result_folder = os.path.join(folder_path, "result")
    os.makedirs(result_folder, exist_ok=True)

    metadata_path = os.path.join(folder_path, "metadata.json")
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    reencoded_videos = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(reencode_video_concurrent, os.path.join(folder_path, file), folder_path): file for file in video_files}

        for future in concurrent.futures.as_completed(futures):
            reencoded_path = future.result()
            if reencoded_path:
                reencoded_videos.append(reencoded_path)

    if not reencoded_videos:
        print("⚠️ No valid videos to merge.")
        return None

    clips = []
    for video_path in reencoded_videos:
        try:
            clip = VideoFileClip(video_path)
            filename = os.path.basename(video_path).replace("reencoded_", "")
            title = metadata.get(filename, "Unknown Title")  # Retrieve original Reddit title
            clip = add_text_overlay(clip, title)  # Add overlay
            clips.append(clip)
        except Exception as e:
            print(f"❌ Error processing {video_path}: {e}")

    if clips:
        final_video = concatenate_videoclips(clips, method="chain")
        output_path = os.path.join(result_folder, "result.mp4")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4)
        
        aws_client.upload_to_s3(output_path)
        
        print(f"✅ Videos stitched successfully! Output: {output_path}")
        return output_path
    else:
        print("⚠️ No valid video clips to merge.")
        return None
