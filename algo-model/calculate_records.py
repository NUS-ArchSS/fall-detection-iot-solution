import os
import codecs

# Total number of lines: 555453
# Define the directory to search
rootdir = '/Users/huanglh/Downloads/Tests-1/101/'

# Initialize a counter for the total number of lines
total_lines = 0

# Iterate over the directory and its subdirectories
for subdir, dirs, files in os.walk(rootdir):
    # Iterate over the files in the current subdirectory
    for file in files:
        # Check if the file is a text file
        if file.endswith('.txt'):
            # Read the file as Unicode
            with codecs.open(os.path.join(subdir, file), 'r', encoding='utf-8', errors='ignore') as f:
                # Count the number of lines in the file
                num_lines = sum(1 for line in f)
                # Add the number of lines to the total
                total_lines += num_lines

# Print the total number of lines
print(f'Total number of lines: {total_lines}')
