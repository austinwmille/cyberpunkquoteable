# this script combines an audio file, a video file, and a txt file to create a basic, short
#video that will loop and the txt file contains the text that fades on to the screen

import os
import random
import subprocess
import textwrap

# Directories for your assets
quotes_folder = "filtered_quotes"
videos_folder = "cyberpunk"
audio_folder = "audio"
output_folder = "output_videos"
os.makedirs(output_folder, exist_ok=True)

def get_random_neon_color():
    # Randomly pick a neon-like color for variety
    neon_colors = ["#ff007f", "#00ffcc", "#ff4d00", "#8f00ff", "#00ff00", "#00aaff", "#ff66b2", "#ccff33", "#ff3300", "#80e0ff", "#b3aaff", "#ffcccc"]

    return random.choice(neon_colors)

def create_video_with_text_overlay(quote_text, background_video, background_music, output_path):
    # Wrap the text to ensure it fits within the video frame
    wrapped_text = textwrap.fill(quote_text, width=40)  # Adjust width as needed
    neon_color = get_random_neon_color()  # Pick a random neon color for the text overlay

    # Temporary text overlay file
    with open("temp_quote.txt", "w", encoding='utf-8') as temp_file:
        temp_file.write(wrapped_text)
    
    # FFmpeg command to combine video, audio, and text overlay
    ffmpeg_command = [
        "ffmpeg",
        "-stream_loop", "-1",
        "-i", background_video,
        "-i", background_music,
        "-vf",
        "crop=ih*9/16:ih, "  # Crop the video to 9:16 aspect ratio without stretching
        "scale=1080:1920, "  # Scale to fit 1080x1920 for vertical aspect
        "drawtext=fontfile='C\\:/Windows/Fonts/Gabriola.ttf':"
        "textfile=temp_quote.txt:"
        "fontcolor=white:"
        "fontsize=36:"
        "line_spacing=10:"  # Adjust line spacing for readability
        "x=(w-text_w)/2:"
        "y=(h-text_h)/2:"
        "box=1:"
        "boxcolor=black@0.4:"
        "boxborderw=17:"
        "borderw=2:"
        f"bordercolor={neon_color}:"  # Apply the random neon color here
        f"shadowcolor={neon_color}@0.15:"  # Apply a matching neon shadow color
        "shadowx=2:"
        "shadowy=2:"
        "alpha='if(lt(t,1), 0, if(lt(t,5), (t-1)/4, if(lt(t,10), 1, if(lt(t,13), 1-(t-10)/3, 0))))'",  # Smoother fade out
        "-t", "15",  # Extended duration to 15 seconds
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]
    
    # Run the FFmpeg command
    subprocess.run(ffmpeg_command, check=True)

# Main function to combine files and create videos
def generate_videos():
    quote_files = [f for f in os.listdir(quotes_folder) if f.endswith(".txt")]
    video_files = [f for f in os.listdir(videos_folder) if f.endswith((".mp4", ".mov"))]
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith((".mp3", ".wav"))]
    
    for quote_file in quote_files:
        # Randomly pick one video and one audio file for each quote
        video_file = random.choice(video_files)
        audio_file = random.choice(audio_files)
        
        # Load the quote text
        with open(os.path.join(quotes_folder, quote_file), "r", encoding='utf-8') as file:
            quote_text = file.read().strip()
        
        # Create a descriptive output filename
        output_filename = f"{quote_file.replace('.txt', '')}_{video_file.replace('.mp4', '')}_{audio_file.replace('.mp3', '')}.mp4"
        output_path = os.path.join(output_folder, output_filename)
        
        # Create video with text overlay
        create_video_with_text_overlay(quote_text, os.path.join(videos_folder, video_file), os.path.join(audio_folder, audio_file), output_path)
        
        print(f"Created video: {output_filename}")

# Run the video generation function
generate_videos()
