import os
import requests

# API endpoint for ZenQuotes
api_url = "https://zenquotes.io/api/quotes"

# Number of quotes to fetch (increased to improve chances of finding matches)
num_quotes = 200
batch_size = 50  # ZenQuotes returns 50 quotes per request, so we'll make multiple requests if needed

# Expanded list of keywords to filter quotes
keywords = [
    "technology", "future", "innovation", "progress", "humanity", "cyber", "digital", 
    "science", "change", "knowledge", "wisdom", "possibilities", "growth", "imagination", 
    "creation", "dream", "explore", "potential", "evolve"
]

# Create a folder to store the filtered quotes if it doesn't exist
os.makedirs("filtered_quotes", exist_ok=True)

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
        # Check if any keyword is present in the quote text
        if any(keyword in quote_text for keyword in keywords):
            filtered_quotes.append(quote_data)
    return filtered_quotes

def save_filtered_quotes_to_files(filtered_quotes):
    for i, quote_data in enumerate(filtered_quotes, start=1):
        quote_text = quote_data.get("q", "No quote found")
        author = quote_data.get("a", "Unknown")
        
        # Save each filtered quote in a separate file
        filename = f"filtered_quotes/quote_{i}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"\"{quote_text}\"\n")
            file.write(f"– {author}\n")
        print(f"Saved: {filename}")

# Fetch quotes, filter them, and save the filtered quotes to text files
quotes = fetch_quotes()
filtered_quotes = filter_quotes(quotes)
if filtered_quotes:
    save_filtered_quotes_to_files(filtered_quotes)
    print("All filtered quotes have been saved successfully.")
else:
    print("No quotes matched the specified keywords.")
