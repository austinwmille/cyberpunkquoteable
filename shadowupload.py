import os
import time
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Path to your OAuth 2.0 Client ID JSON file
CLIENT_SECRET_FILE = 'path to secret'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Updated authentication function
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

# Directories for videos and quotes
videos_folder = "./output_videos"  # Folder where videos are stored
quotes_folder = "./quotes"  # Folder where quotes (.txt files) are stored
uploaded_folder = './uploaded to youtube'  # Folder for uploaded videos
os.makedirs(uploaded_folder, exist_ok=True)

# Tags list
tags = ["ShadowsInNeon", "Cyberpunk", "TechReflections", "FuturisticVibes", "NeonDreams", "Shorts"]

# Function to generate a clean title for YouTube
def generate_clean_title(video_file):
    base_name = os.path.splitext(video_file)[0]
    parts = base_name.split('_')
    
    clean_title = parts[0]
    if len(parts) > 1 and parts[1].isdigit():
        clean_title += f" {parts[1]}"
    
    return f"Reflections in Neon: {clean_title}"

# Function to retrieve the matching quote for a video
def get_quote_for_video(video_file):
    parts = video_file.split('_')
    base_name = parts[0]
    number_part = parts[1] if len(parts) > 1 and parts[1].isdigit() else ""
    quote_filename = f"{base_name}_{number_part}.txt" if number_part else f"{base_name}.txt"
    quote_file_path = os.path.join(quotes_folder, quote_filename)
    
    if os.path.exists(quote_file_path):
        with open(quote_file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    print(f"No matching quote file found for video: {video_file}")
    return None

# Function to create the video title and description
def generate_title_and_description(video_file):
    quote = get_quote_for_video(video_file)
    title = generate_clean_title(video_file)  # Use the clean title function here
    description = f"{quote}\n\n\nThis video is part of the Neon Reflections series, blending cyberpunk visuals with thought-provoking quotes about life, growth, and the future.\n#CyberpunkQuotes #NeonReflections #FutureThoughts"
    return title, description

# Function to upload video to YouTube
def upload_video(youtube, file_path, title, description):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22',  # Category ID 24 is for "Entertainment", 22 is "People & Blogs"
        },
        'status': {
            'privacyStatus': 'private'
        }
    }
    media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading {file_path}: {int(status.progress() * 100)}%")
    print(f"Upload completed: {title}")
    return response

# Main function to process all videos
def main():
    youtube = get_authenticated_service()
    video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.mov'))]
    
    upload_count = 0
    max_test_uploads = 4
    
    for video_file in video_files:
        if upload_count >= max_test_uploads:
            break
        
        file_path = os.path.join(videos_folder, video_file)
        title, description = generate_title_and_description(video_file)
        
        print(f"Starting upload for: {file_path}")
        upload_video(youtube, file_path, title, description)
        
        # Move the uploaded video to 'uploaded to youtube' folder
        try:
            shutil.move(file_path, os.path.join(uploaded_folder, video_file))
            print(f"Moved {file_path} to {uploaded_folder}")
        except Exception as e:
            print(f"Failed to move {file_path} to {uploaded_folder}: {e}")
        
        upload_count += 1
        time.sleep(30)  # Wait between uploads to manage quota

if __name__ == '__main__':
    main()
