# given a folder containing txt files, this script will choose two at random
#and move them to a subfolder. it does this until there are no more pairs

import os
import shutil

# Define the folder paths relative to the script's location
quotes_folder = os.getcwd()  # The current folder where the script and quote files are located
sorted_folder = os.path.join(quotes_folder, "sorted quotes")
os.makedirs(sorted_folder, exist_ok=True)

# Get all text files in the quotes folder, sorted for proper pairing
quote_files = sorted([f for f in os.listdir(quotes_folder) if f.endswith('.txt')])

# Pair every two quotes and organize into subfolders within the quotes folder
pair_count = 1
for i in range(0, len(quote_files) - 1, 2):
    # Create a new folder for each pair
    pair_folder = os.path.join(quotes_folder, f"quotepair{pair_count}")
    os.makedirs(pair_folder, exist_ok=True)
    
    # Move the two quotes into the pair folder
    for j in range(2):  # Each pair will contain 2 quotes
        quote_file = quote_files[i + j]
        src_path = os.path.join(quotes_folder, quote_file)
        dest_path = os.path.join(pair_folder, quote_file)
        shutil.move(src_path, dest_path)

    pair_count += 1

# Move any remaining unpaired quotes to the sortedquotes folder

# deleted this part to keep unused quotes

print("Quotes paired and organized successfully.")
