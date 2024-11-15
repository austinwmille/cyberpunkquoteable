import os
import re

# Directories for the quotes (text files) and videos
quotes_folder = "./quotes"  # Replace with the path to your quotes folder
videos_folder = "./output_videos"  # Replace with the path to your videos folder

# List of titles to use for renaming (order must match the order of video files)
titles = [
    "Embracing Change to Avoid Disaster",
    "Life: A Dream Unfolding",
    "The Essence of Human Behavior",
    "Changing Circumstances, Changing Attitudes",
    "Shaping Tomorrow with Today’s Choices",
    "Daydreams and Hidden Realities",
    "Awakening Through Inner Vision",
    "Dreams Over Memories",
    "From Prisoner of the Past to Architect of the Future",
    "The Power of a Changed Mind",
    "Pulse of the Future",
    "Vision Beyond Horizons",
    "Strength in Silence",
    "Journey Through Time",
    "Reflective Echoes",
    "Infinite Dreams",
    "Resilience in Shadows",
    "Paths of Destiny",
    "Silent Connections",
    "Fragments of Knowledge",
    "Unveiling Mystery",
    "Embrace the Solitude",
    "Awakening the Courage Within",
    "Chasing the Neon Lights"
]

# Function to clean up title for valid filenames
def clean_title(title):
    # Remove invalid characters and strip whitespace/newlines
    return re.sub(r'[\\/*?:"<>|\n\r]', "", title).strip()

# Get sorted list of video files in the directory
video_files = sorted([f for f in os.listdir(videos_folder) if f.endswith((".mp4", ".mov", ".avi"))])  # Update extensions if needed

# Check if there’s a mismatch in the number of titles and video files
if len(titles) != len(video_files):
    print("The number of titles does not match the number of videos.")
else:
    # Rename each video based on the corresponding title
    for i in range(len(video_files)):
        # Clean the title and create the new video filename
        clean_filename = clean_title(titles[i]) + os.path.splitext(video_files[i])[1]
        video_path = os.path.join(videos_folder, video_files[i])
        new_video_path = os.path.join(videos_folder, clean_filename)
        
        # Rename the video file
        os.rename(video_path, new_video_path)
        print(f"Renamed '{video_files[i]}' to '{clean_filename}'")

    print("All videos have been renamed successfully.")
