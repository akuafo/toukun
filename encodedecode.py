import sys
from encodedecodemodule import encode_string, decode_token

def display_encoding_results(encoded_results):
    print("\nTikToken results:")
    print(f"Array of tokens of length {len(encoded_results)}:")
    for result in encoded_results:
        print(f"    integer: {result['integer']} | string: {result['string']} | byte literal: {result['byte_literal']}")

def display_decoding_results(decoded_result):
    print("\nTikToken results:")
    if isinstance(decoded_result, str):
        print(decoded_result)
    else:
        print(f"  array value: {decoded_result['array_value']} | decode to string: {decoded_result['decode_to_string']} | decode to byte literal: {decoded_result['decode_to_byte_literal']}")

def main():
    while True:
        user_input = input("Please enter a command: \n  ('s' to input string, 't' to input token', or 'q' to quit) \n")

        if user_input.lower() in ['quit', 'q']:
            break
        elif user_input.lower() == 's':
            string_to_encode = input("Enter a string to encode: ")
            encoded_results = encode_string(string_to_encode)
            display_encoding_results(encoded_results)
        elif user_input.lower() == 't':
            token_to_decode = input("Enter a token to decode (integer): ")
            decoded_result = decode_token(token_to_decode)
            display_decoding_results(decoded_result)
        else:
            print(f"Unknown command: {user_input}")

main()
