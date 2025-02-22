from src.handler.merge_handler import stitch_videos_in_folder

def merge_controller(folder_path):
    return stitch_videos_in_folder(folder_path)

if __name__ == "__main__":
    folder_path = input("Enter folder path: ").strip()
    merge_controller(folder_path)
