# This python script will write out several files that help to understand the tiktoken dictionary, encoding, and parsing.
# The files are saved to the directory 'referencefiles'

import tiktoken
import urllib.request
import base64
import time
import os
import datetime

def list_files_in_dir(directory):
    print(f'{"File Name":<50} {"File Size":<10} {"Last Modified"}')
    print('-' * 80)    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        size = os.path.getsize(filepath)
        modified_time = os.path.getmtime(filepath)
        modified_time = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f'{filename:<50} {size:<10} {modified_time}')

print("\nThis script will write files to /referencefiles.  Initially, the directory is empty.")
print("")
list_files_in_dir("referencefiles")
print("")

encoding = tiktoken.get_encoding("cl100k_base")  # Using the cl100k_base model.

print("We'll set the tiktoken model as 'cl100k_base model' since that model is used for GPT-4.")
print("Next, this will write the raw tiktoken dictionary file which consists of base64 encoded tokens and their index numbers.")
print("The source file is at this URL:  https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken")

url = "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
file_path = "referencefiles/cl100k_base.tiktoken"

urllib.request.urlretrieve(url, file_path)

print("")
list_files_in_dir("referencefiles")
print("")

    
print("This step will convert the text-related values in the cl100k_base file and output two additional files.")

print("For the next output file, the bash64 values will be decoded to display the byte literals.  ")
print("For example, the letter A becomes the string literal b'A'.")

print("For the next output file, the base64 values will be decoded into UTF-8 strings in order to see double-byte characters.")
print("  For example, character 22656 is the byte literal b'\xe6\x9c\xac' which corresponds to the Japanese kanji 本.")
print("  Sometimes the bytes are not valid UTF-8 so it substitutes the default 'replace' unicode character.")
print("  Sometimes there will be formatting characters like carriage returns that will display weirdness in a text editor.")
print("  cl100k_base_byteliterals.txt and cl100k_base_utf8.txt have been written successfully.")

with open('referencefiles/cl100k_base.tiktoken', 'r') as infile, \
     open('referencefiles/cl100k_base_byteliterals.txt', 'w') as outfile_bytes, \
     open('referencefiles/cl100k_base_utf8.txt', 'w') as outfile_utf8:
    for line in infile:
        b64_value, number = line.strip().split()  # Split the line into the base64 value and the number
        decoded_bytes = base64.b64decode(b64_value)  # Decode the base64 value
        outfile_bytes.write(f"{number} {decoded_bytes}\n")  # Write the byte string literal to the first output file
        decoded_string = decoded_bytes.decode('utf-8', errors='replace')  
        outfile_utf8.write(f"{number} {decoded_string}\n")  # Write the UTF-8 string to the second output file

print("")
list_files_in_dir("referencefiles")
print("")
