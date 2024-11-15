import requests
import os

# Azure Speech API setup with stored region and key
api_key = "path to secrets"
region = "eastus"
endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"

# Set up file paths
quote_file = r"path to folder containing folders qhich contain two txt files"  # Path to the text file with the quote
output_audio_path = "quote_with_speaker_azure_calm_tone.wav"  # Path to save the final audio file
pause_duration = 37  # Pause duration before speaker name

# Read quote and speaker from the text file
with open(quote_file, 'r') as file:
    lines = file.readlines()
    quote_text = lines[0].strip()
    speaker_name = lines[1].strip() if len(lines) > 1 else "Unknown"

# SSML structure with minimal pause and calm tone
ssml_text = f"""
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-ChristopherNeural">  <!-- Male voice with a serious, calm tone -->
    <prosody rate="medium" pitch="-5%">  <!-- Decreased pitch for a serious tone -->
      Change<break time="0.15ms"/> is never easy, but always possible.
    </prosody>
    <break time="{pause_duration}ms"/>
    <prosody rate="medium" pitch="-5%">{speaker_name}</prosody>  <!-- Consistent pitch for speaker name -->
  </voice>
</speak>
"""

# Headers for the API request
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm"
}

# Make the request to Azure TTS
response = requests.post(endpoint, headers=headers, data=ssml_text)

# Check if the request was successful
if response.status_code == 200:
    # Save the audio to a file
    with open(output_audio_path, "wb") as audio_file:
        audio_file.write(response.content)
    print(f"Audio generated successfully and saved to {output_audio_path}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
