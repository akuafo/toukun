# Purpose of this test:  Test tiktoken encoding and decoding and counting from the command line

import tiktoken
import time
import regex

encoding = tiktoken.get_encoding("cl100k_base")  # Using the cl100k_base model.

def command_s():
    user_input = input("Enter a string to encode: ")
    print("  Titoken results:"); time.sleep(1)
    print("  array of tokens of length " + str(len(encoding.encode(user_input)))); time.sleep(1)
    for t in encoding.encode(user_input):  #for each token in the token array
        print("    token as integer: " + str(t) + " | token as string: " + encoding.decode([t]) + " | token as byte literal: " + str(encoding.decode_bytes([t]))); time.sleep(1)

## decoded_string = decoded_bytes.decode('utf-8', errors='replace')  

def command_t():
    user_input = input("Enter a token to decode (integer: ")
    if not regex.match(r'^\d+$', user_input):
        print("  Error:  Input must be an integer.")
        return
    t = [int(user_input)]
    print("  Titoken results:"); time.sleep(1)
    print("  array value: " + str(t) + " | decode to string: " + str(encoding.decode(t))+ " | decode to byte literal: " + str(encoding.decode_bytes(t))); 
    
commands = {
    's': command_s,
    't': command_t,
}

while True:
    user_input = input("Please enter a command ('s' to input string, 't' to input token', or 'q' to quit): \n")
    if user_input.lower() in ['quit', 'q']:
        break
    elif user_input.lower() in commands:
        commands[user_input.lower()]()
        print("")
    else:
        print(f"Unknown command: {user_input}")

# sample string:  "版本"
# sample tokens:  0, 32, 16508, 22656, 33334, 33406
