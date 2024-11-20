import os
import hashlib
import requests

# API endpoint for ZenQuotes
api_url = "https://zenquotes.io/api/quotes"

# Number of quotes to fetch
num_quotes = 800
batch_size = 50

# Keywords to filter quotes
keywords = [
    "technology", "future", "innovation", "progress", "humanity", "cyber", "digital", 
    "science", "change", "knowledge", "wisdom", "possibilities", "growth", "imagination", 
    "creation", "dream", "explore", "potential", "evolve", "artificial", "intelligence", 
    "cyberspace", "quantum", "hacker", "virtual", "revolution", "metaverse", "synth", 
    "futureproof", "anarchy", "dystopia", "utopia", "circuitry", "glitch", "resistance", 
    "augmented", "neural", "interface", "biotech", "chrome", "megacity", "noir", "shadow", 
    "matrix", "transcendence"
]

# Create folder and tracking file
os.makedirs("filtered_quotes", exist_ok=True)
downloaded_quotes_file = "downloaded_quotes.txt"
if not os.path.exists(downloaded_quotes_file):
    open(downloaded_quotes_file, "w").close()

def hash_quote(text):
    """Generate a hash for the given quote text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def is_duplicate(quote_text):
    """Check if the quote is already saved."""
    quote_hash = hash_quote(quote_text)
    with open(downloaded_quotes_file, "r", encoding="utf-8") as file:
        return quote_hash in file.read()

def save_quote_hash(quote_text):
    """Save the quote hash to the tracking file."""
    quote_hash = hash_quote(quote_text)
    with open(downloaded_quotes_file, "a", encoding="utf-8") as file:
        file.write(quote_hash + "\n")

def get_next_filename():
    """Find the next available filename to avoid overwriting."""
    existing_files = os.listdir("filtered_quotes")
    existing_numbers = [
        int(filename.split("_")[1].split(".")[0]) for filename in existing_files if filename.startswith("quote_")
    ]
    next_number = max(existing_numbers, default=0) + 1
    return f"filtered_quotes/quote_{next_number}.txt"

def fetch_quotes():
    quotes = []
    for _ in range((num_quotes + batch_size - 1) // batch_size):  # Number of batches to fetch
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            quotes.extend(data)
        else:
            print(f"Failed to fetch quotes. Status Code: {response.status_code}")
            break
    return quotes[:num_quotes]  # Return the exact number of quotes specified

def filter_quotes(quotes):
    filtered_quotes = []
    for quote_data in quotes:
        quote_text = quote_data.get("q", "").lower()
        # Check if any keyword is present and the quote is not a duplicate
        if any(keyword in quote_text for keyword in keywords) and not is_duplicate(quote_text):
            filtered_quotes.append(quote_data)
    return filtered_quotes

def save_filtered_quotes_to_files(filtered_quotes):
    for quote_data in filtered_quotes:
        quote_text = quote_data.get("q", "No quote found")
        author = quote_data.get("a", "Unknown")
        
        # Generate a unique filename
        filename = get_next_filename()
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"\"{quote_text}\"\n")
            file.write(f"– {author}\n")
        save_quote_hash(quote_text)
        print(f"Saved: {filename}")

# Fetch quotes, filter them, and save the filtered quotes to text files
quotes = fetch_quotes()
filtered_quotes = filter_quotes(quotes)
if filtered_quotes:
    save_filtered_quotes_to_files(filtered_quotes)
    print("All filtered quotes have been saved successfully.")
else:
    print("No new quotes matched the specified keywords.")
