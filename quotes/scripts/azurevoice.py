import requests
import os

# Azure Speech API setup with stored region and key
api_key = "azure api key here"
region = "eastus"
endpoint = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"

# Base directory where the quotepairs are located
base_dir = r"path to a folder that contains quote pairs"
pause_duration = 150  # Pause duration before speaker name
short_pause = 0       # Short pause after the first word

# Function to generate audio for a single quote
def generate_audio(quote_text, speaker_name, output_path):
    # SSML structure with tiny pause after first word and calm tone
    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
      <voice name="en-US-ChristopherNeural">  <!-- Male voice with a serious, calm tone -->
        <prosody rate="medium" pitch="-5%">  <!-- Decreased pitch for a serious tone -->
          {quote_text.split()[0]}<break time="{short_pause}ms"/> {' '.join(quote_text.split()[1:])}.
        </prosody>
        <break time="{pause_duration}ms"/>
        <prosody rate="medium" pitch="-5%">{speaker_name}</prosody>  <!-- Consistent pitch for speaker name -->
      </voice>
    </speak>
    """

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm"
    }

    # Send request to Azure TTS
    response = requests.post(endpoint, headers=headers, data=ssml_text)

    # Check if response is successful and print details for debugging
    if response.status_code == 200:
        with open(output_path, "wb") as audio_file:
            audio_file.write(response.content)
        print(f"Audio generated successfully and saved to {output_path}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Process each quotepair folder
for folder in os.listdir(base_dir):
    quotepair_path = os.path.join(base_dir, folder)
    if os.path.isdir(quotepair_path) and folder.startswith("quotepair"):
        print(f"\nProcessing {quotepair_path}...")  # Debugging line
        temp_audio_path = os.path.join(quotepair_path, "temp_audio")
        os.makedirs(temp_audio_path, exist_ok=True)

        # Find all quote files in the quotepair folder
        for quote_file in os.listdir(quotepair_path):
            if quote_file.startswith("quote") and quote_file.endswith(".txt"):
                quote_path = os.path.join(quotepair_path, quote_file)
                with open(quote_path, 'r') as file:
                    lines = file.readlines()
                    if len(lines) >= 1:
                        quote_text = lines[0].strip()
                        speaker_name = lines[1].strip() if len(lines) > 1 else "Unknown"

                        # Define the output path for the individual audio file
                        audio_output_path = os.path.join(temp_audio_path, f"{quote_file.replace('.txt', '')}_audio.wav")
                        print(f"Generating audio for {quote_file} in {quotepair_path}...")  # Debugging line
                        generate_audio(quote_text, speaker_name, audio_output_path)
                    else:
                        print(f"No content found in {quote_file}")
