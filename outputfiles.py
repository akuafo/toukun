# This python script will write out several files that help to understand the tiktoken dictionary, encoding, and parsing.
# The files are saved to the directory 'referencefiles'

import tiktoken
import urllib.request
import base64
import time

encoding = tiktoken.get_encoding("cl100k_base")  # Using the cl100k_base model.

def set_tiktoken_encoding():
    """
    We'll set the tiktoken model as 'cl100k_base model' since that model is used for GPT-4.
    """
print(set_tiktoken_encoding.__doc__); time.sleep(1)

def write_tiktoken_dictionary():
    """
    # File:  cl100k_base.tiktoken
    
    It includes the dictionary of base64 encoded tokens and their index numbers.
    The source file is at this URL:  https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken
    """
    url = "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"  
    urllib.request.urlretrieve(url, "referencefiles/cl100k_base.tiktoken")
print(write_tiktoken_dictionary.__doc__); time.sleep(1)
print("\nSaved file:  referencefiles/cl100k_base.tiktoken\n")

def write_tiktoken_byteliteral_utf8string(): 
    """
    # Files:  cl100k_base_byteliterals.txt, cl100k_base_utf8.txt
    
    This step will convert the text-related values in the cl100k_base file and output two additional files.

    For the first output file, we'll be decoding the bash64 values which will result in byte literals.  
    For example, the letter A becomes the string literal b'A'.

    For the second output file, we'll decode the base64 values into UTF-8 strings so that we can see double-byte characters.
        For example, character 22656 is the byte literal b'\xe6\x9c\xac' which corresponds to the Japanese kanji 本.
        Sometimes the bytes are not valid UTF-8 so it substitutes the default 'replace' unicode character.
        Sometimes there will be formatting characters like carriage returns that will display weirdness in a text editor.
        cl100k_base_byteliterals.txt and cl100k_base_utf8.txt have been written successfully.
    """
with open('referencefiles/cl100k_base.tiktoken', 'r') as infile, \
     open('referencefiles/cl100k_base_byteliterals.txt', 'w') as outfile_bytes, \
     open('referencefiles/cl100k_base_utf8.txt', 'w') as outfile_utf8:
    for line in infile:
        b64_value, number = line.strip().split()  # Split the line into the base64 value and the number
        decoded_bytes = base64.b64decode(b64_value)  # Decode the base64 value
        outfile_bytes.write(f"{number} {decoded_bytes}\n")  # Write the byte string literal to the first output file
        decoded_string = decoded_bytes.decode('utf-8', errors='replace')  
        outfile_utf8.write(f"{number} {decoded_string}\n")  # Write the UTF-8 string to the second output file
print(write_tiktoken_byteliteral_utf8string.__doc__); time.sleep(1)
