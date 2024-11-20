import os
import re

# Directories for quotes and videos
quotes_folder = "./filtered_quotes"
videos_folder = "./output_videos"

# Function to clean up title for valid filenames
def clean_title(title):
    return re.sub(r'[\\/*?:"<>|\n\r]', "", title).strip()

# Function to generate a title from a quote
def generate_title(quote):
    # Define keywords and titles (from quotetitle.py)
    keywords = {
        "change": "Embracing Change",
        "future": "A Glimpse into Tomorrow",
        "dream": "Life in Dreams",
        # Add all other keywords here...
    }
    combined_titles = {
        ("change", "future"): "Change for Tomorrow",
        ("dream", "technology"): "Technological Dreams",
        # Add all other combinations here...
    }

    # Find matching keywords in the quote
    found_keywords = [word for word in keywords if re.search(rf"\b{word}\b", quote, re.IGNORECASE)]

    # Determine title
    if not found_keywords:
        return "Inspiring Thoughts"
    if len(found_keywords) == 1:
        return keywords[found_keywords[0]]
    for combination, title in combined_titles.items():
        if all(word in found_keywords for word in combination):
            return title
    return "Reflections in Neon"

# Process videos and generate titles
quote_files = sorted([f for f in os.listdir(quotes_folder) if f.endswith(".txt")])
video_files = sorted([f for f in os.listdir(videos_folder) if f.endswith((".mp4", ".mov", ".avi"))])

if len(quote_files) != len(video_files):
    print("The number of quote files does not match the number of videos.")
else:
    for i, video in enumerate(video_files):
        # Read the quote text
        with open(os.path.join(quotes_folder, quote_files[i]), "r", encoding="utf-8") as file:
            quote_text = file.read().strip()

        # Generate title from the quote
        title = generate_title(quote_text)
        clean_filename = clean_title(title) + os.path.splitext(video)[1]

        # Rename the video file
        video_path = os.path.join(videos_folder, video)
        new_video_path = os.path.join(videos_folder, clean_filename)
        os.rename(video_path, new_video_path)
        print(f"Renamed '{video}' to '{clean_filename}'")

    print("All videos have been renamed successfully.")
