import boto3
import os

# Initialize Amazon Polly client
polly = boto3.client('polly')

# Set up file paths
quote_file = r"path to a txt file that contains a quote"  # Path to the text file with the quote
output_audio_path = "quote_with_speaker.mp3"  # Path to save the final audio file
voice_id = "Matthew"  # Select voice for Polly
pause_duration = 0.5  # Pause duration (in seconds) before the speaker's name

# Read quote and speaker from the text file
with open(quote_file, 'r') as file:
    lines = file.readlines()
    quote_text = lines[0].strip()
    speaker_name = lines[1].strip() if len(lines) > 1 else "Unknown"  # Assuming speaker's name is on the second line

# Create SSML with a pause before the speaker's name, making the speaker's name slower
ssml_text = f"<speak><prosody rate='medium' pitch='-2%'>{quote_text}</prosody>" \
            f"<break time='{int(pause_duration * 1000)}ms'/>" \
            f"<prosody rate='x-slow'>{speaker_name}</prosody></speak>"

# Convert text to speech
response = polly.synthesize_speech(
    Text=ssml_text,
    TextType="ssml",
    VoiceId=voice_id,
    OutputFormat="mp3"
)

# Save audio file
with open(output_audio_path, 'wb') as file:
    file.write(response['AudioStream'].read())

print(f"Audio generated successfully and saved to {output_audio_path}")
