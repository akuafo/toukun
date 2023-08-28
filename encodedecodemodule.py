import tiktoken
import regex

encoding = tiktoken.get_encoding("cl100k_base")  # Using the cl100k_base model

def encode_string(user_input):
    results = []
    for t in encoding.encode(user_input):  # for each token in the token array
        results.append({
            'integer': t,
            'string': encoding.decode([t]),
            'byte_literal': encoding.decode_bytes([t]),
        })
    return results

def decode_token(user_input):
    if not regex.match(r'^\d+$', user_input):
        return "Input must be an integer."
    t = [int(user_input)]
    return {
        'array_value': t,
        'decode_to_string': encoding.decode(t),
        'decode_to_byte_literal': encoding.decode_bytes(t),
    }
