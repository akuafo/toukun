# Purpose of this test:  Test tiktoken encoding and decoding and counting from the command line

import tiktoken
import time
import openai
import regex

encoding = tiktoken.get_encoding("cl100k_base")  # Using the cl100k_base model.

def command_s():
    print("\nExecuting command s...")
    user_input = input("Enter a string to encode: ")
    print("  Titoken results:"); time.sleep(1)
    print("  array of tokens of length " + str(len(encoding.encode(user_input)))); time.sleep(1)
    for t in encoding.encode(user_input):  #for each token in the token array
        print("    token as integer: " + str(t) + " | token as string: " + encoding.decode([t]) + " | token as byte literal: " + str(encoding.decode_bytes([t]))); time.sleep(1)

## decoded_string = decoded_bytes.decode('utf-8', errors='replace')  

def command_t():
    print("\nExecuting command t...")
    user_input = input("Enter a token to decode: ")
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
     

# model="gpt-4-0314"  #cl100k_base

# t = 9019
# print("  tiktoken token: " + str(t) + " | tiktoken string: " + encoding.decode([t]) + " | tiktoken byte literal: " + str(encoding.decode_bytes([t])))

# time.sleep(1)

# print("+ " + str(len(encoding.encode(value))) + " tokens for json key/value pair: " + key + " | " + value + " " + str(encoding.encode(value))); time.sleep(1)
#print("string in json is encoded by tiktoken into token and then decoded into string: " + encoding.decode(encoding.encode(value)))
# for t in encoding.encode(value):  #for each token in the token array
#     print("  tiktoken token: " + str(t) + " | tiktoken string: " + encoding.decode([t]) + " | tiktoken byte literal: " + str(encoding.decode_bytes([t])))
# num_tokens += len(encoding.encode(value))
# if key == "name":
#     num_tokens += tokens_per_name
#     print("+ 1 token per name:  " + value); time.sleep(1)


# sample text:  "a 版本"
# sample tokens:  0, 32, 16508, 22656, 33334, 33406
