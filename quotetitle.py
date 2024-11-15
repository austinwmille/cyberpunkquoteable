import os
import re

# Directory containing the .txt files with quotes
directory = "quotes"  # Replace with your directory path

# Dictionary of keywords with associated titles, ordered by priority
keywords = {
    "change": "Embracing Change",
    "future": "A Glimpse into Tomorrow",
    "dream": "Life in Dreams",
    "behavior": "Understanding Human Behavior",
    "attitude": "The Power of Attitude",
    "technology": "The Pulse of Progress",
    "wisdom": "Fragments of Wisdom",
    "journey": "The Path Unfolds",
    "strength": "Strength in Shadows",
    "reflection": "Echoes of Reflection",
    "purpose": "Purpose in Motion",
    "growth": "Evolving Forward",
    "freedom": "Unlocking Freedom",
    "courage": "The Heart of Courage",
    "resilience": "Built to Endure",
    "mystery": "Shadows and Light",
    "truth": "The Search for Truth",
    "knowledge": "Illumination Through Knowledge",
    "possibility": "Infinite Possibilities",
    "darkness": "Through the Darkness",
    "light": "Chasing the Light",
    "solitude": "In Solitude's Embrace",
    "hope": "The Edge of Hope",
    "connection": "Web of Connections",
    "destiny": "Forging Destiny",
    "peace": "Silent Peace",
    "self": "Discovering the Self",
    "imagination": "Limits of Imagination"
    # Add additional keywords with titles as needed
}

# Define custom titles for specific combinations of keywords
combined_titles = {
    ("change", "future"): "Change for Tomorrow",
    ("dream", "technology"): "Technological Dreams",
    ("strength", "resilience"): "Strength and Resilience",
    ("freedom", "connection"): "Connected Freedom",
    ("light", "darkness"): "Light in the Darkness",
    ("hope", "destiny"): "Fate’s Whisper",
    ("truth", "mystery"): "Veil of Secrets",
    ("knowledge", "wisdom"): "Fragments of the Unknown",
    ("journey", "solitude"): "Path of Shadows",
    ("reflection", "purpose"): "Echoes of Purpose",
    ("self", "imagination"): "Within the Mind's Eye",
    ("growth", "courage"): "Seeds of Bravery",
    ("peace", "solitude"): "Whispers in Silence",
    ("destiny", "strength"): "Bound by Fate",
    ("imagination", "future"): "Dreams of the Unreal",
    ("light", "hope"): "A Flicker Beyond",
    ("truth", "connection"): "Threads of Reality",
    ("knowledge", "mystery"): "Ancient Light",
    ("freedom", "purpose"): "Boundless Intent",
    ("darkness", "journey"): "Walk Through Shadows",
    ("self", "reflection"): "Mirror of the Unknown"
}

# Function to generate a title based on found keywords
def generate_title(quote):
    found_keywords = [word for word in keywords if re.search(rf"\b{word}\b", quote, re.IGNORECASE)]
    
    # If no keywords match, return a default title
    if not found_keywords:
        return "Inspiring Thoughts"
    
    # If only one keyword is found, return its associated title
    if len(found_keywords) == 1:
        return keywords[found_keywords[0]]
    
    # If multiple keywords are found, check for specific combinations
    for combination, title in combined_titles.items():
        if all(word in found_keywords for word in combination):
            return title
    
    # Default action if multiple keywords are found but no specific combination matches
    return "Reflections in Neon"  # Default title for multiple unmatched keywords

# Function to ensure unique filenames in the directory
def get_unique_filename(directory, base_name):
    counter = 1
    new_filename = f"{base_name}.txt"
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base_name}_{counter}.txt"
        counter += 1
    return new_filename

# Process each .txt file in the directory and rename based on the generated title
def rename_files_with_titles(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                quote = file.read().strip()
            
            # Generate title based on keywords found
            title = generate_title(quote)
            
            # Clean up title for a valid filename
            base_name = re.sub(r'[\\/*?:"<>|]', "", title)
            new_filename = get_unique_filename(directory, base_name)
            new_filepath = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(filepath, new_filepath)
            print(f"Renamed '{filename}' to '{new_filename}'")

# Run the renaming function
rename_files_with_titles(directory)
