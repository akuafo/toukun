# Copied and modified from /tiktoken/tiktoken/_educational.py which was part of tiktoken release 0.4.0 May 8, 2023.
# This modified version is messier than the tiktoken original _educational.py but is intended to be a bit more clear.

"""This is an educational implementation of the byte pair encoding algorithm."""
from __future__ import annotations

import collections
import itertools
from typing import Optional

import regex

import tiktoken

import time

class SimpleBytePairEncoding:
    def __init__(self, *, pat_str: str, mergeable_ranks: dict[bytes, int]) -> None:
        """Creates an Encoding object."""
        # A regex pattern string that is used to split the input text
        self.pat_str = pat_str
        # A dictionary mapping token bytes to their ranks. The ranks correspond to merge priority
        self.mergeable_ranks = mergeable_ranks

        self._decoder = {token: token_bytes for token_bytes, token in mergeable_ranks.items()}
        self._pat = regex.compile(pat_str)

    def encode(self, text: str, visualise: Optional[str] = "colour") -> list[int]:
        """Encodes a string into tokens.

        >>> enc.encode("hello world")
        [388, 372]
        """
        # Use the regex to split the text into (approximately) words
        words = self._pat.findall(text)
        print("\ninput text:  ", text) # print text
        print("splits into", len(words), " words:  ", words) # print number of words
        print("using this regex:  ", self._pat) # print regex
        print('') # print blank line
        tokens = []
        for word in words:
            # Turn each word into tokens, using the byte pair encoding algorithm
            word_bytes = word.encode("utf-8")
            word_tokens = bpe_encode(self.mergeable_ranks, word_bytes, visualise=visualise)
            tokens.extend(word_tokens)
        return tokens

    def decode_bytes(self, tokens: list[int]) -> bytes:
        """Decodes a list of tokens into bytes.

        >>> enc.decode_bytes([388, 372])
        b'hello world'
        """
        return b"".join(self._decoder[token] for token in tokens)

    def decode(self, tokens: list[int]) -> str:
        """Decodes a list of tokens into a string.

        Decoded bytes are not guaranteed to be valid UTF-8. In that case, we replace
        the invalid bytes with the replacement character "�".

        >>> enc.decode([388, 372])
        'hello world'
        """
        return self.decode_bytes(tokens).decode("utf-8", errors="replace")

    def decode_tokens_bytes(self, tokens: list[int]) -> list[bytes]:
        """Decodes a list of tokens into a list of bytes.

        Useful for visualising how a string is tokenised.

        >>> enc.decode_tokens_bytes([388, 372])
        [b'hello', b' world']
        """
        return [self._decoder[token] for token in tokens]

    @staticmethod
    def train(training_data: str, vocab_size: int, pat_str: str):
        """Train a BPE tokeniser on some data!"""
        mergeable_ranks = bpe_train(data=training_data, vocab_size=vocab_size, pat_str=pat_str)
        return SimpleBytePairEncoding(pat_str=pat_str, mergeable_ranks=mergeable_ranks)

    @staticmethod
    def from_tiktoken(encoding):
        if isinstance(encoding, str):
            encoding = tiktoken.get_encoding(encoding)
        return SimpleBytePairEncoding(
            pat_str=encoding._pat_str, mergeable_ranks=encoding._mergeable_ranks
        )


def bpe_encode(
    mergeable_ranks: dict[bytes, int], input: bytes, visualise: Optional[str] = "colour"
) -> list[int]:
    parts = [bytes([b]) for b in input]
    while True:
        # See the intermediate merges play out!
        print("\n", input, " has ", len(parts), " parts") # print length of parts
        for p in parts: # print parts
            try:
                print(p.decode('utf-8'))
            except UnicodeDecodeError:
                print(p)
        if visualise:
            time.sleep(1) # slow down so the output is readable from the command line
            print('')
            if visualise in ["colour", "color"]:
                visualise_tokens(parts)
            elif visualise == "simple":
                print(parts)

        # Iterate over all pairs and find the pair we want to merge the most
        min_idx = None
        min_rank = None
        for i, pair in enumerate(zip(parts[:-1], parts[1:])):
            time.sleep(.5) #slow down the output
            rank = mergeable_ranks.get(pair[0] + pair[1])
            try:
                print("compare ranks:  ", pair[0].decode('utf-8'), "   ", pair[1].decode('utf-8'), " | rank:  ", rank) # print comparison
            except UnicodeDecodeError:
                print("compare ranks:  ", pair[0], "   ", pair[1], " | rank:  ", rank) # print comparison
            if rank is not None and (min_rank is None or rank < min_rank):
                min_idx = i
                min_rank = rank
                # print("  set new minimum rank:  ", min_rank) # print min_rank

        # If there were no pairs we could merge, we're done!
        if min_rank is None:
            break
        assert min_idx is not None

        # Otherwise, merge that pair and leave the rest unchanged. Then repeat.
        parts = parts[:min_idx] + [parts[min_idx] + parts[min_idx + 1]] + parts[min_idx + 2 :]

    if visualise:
        print()

    tokens = [mergeable_ranks[part] for part in parts]

    return tokens


def bpe_train(
    data: str, vocab_size: int, pat_str: str, visualise: Optional[str] = "colour" 
) -> dict[bytes, int]:
    visualise = '' # remove visualise because the console is too busy, saving to file instead
    # First, add tokens for each individual byte value
    if vocab_size < 2**8:
        raise ValueError("vocab_size must be at least 256, so we can encode all bytes")
    ranks = {}
    for i in range(2**8):
        ranks[bytes([i])] = i

    # Splinter up our data into lists of bytes
    # data = "Hello world"
    # words = [
    #     [b'H', b'e', b'l', b'l', b'o'],
    #     [b' ', b'w', b'o', b'r', b'l', b'd']
    # ]
    words: list[list[bytes]] = [
        [bytes([b]) for b in word.encode("utf-8")] for word in regex.findall(pat_str, data)
    ]

    print("Training completed.  The BPT training steps are saved at:  referencefiles/bpetrainingoutput.txt")
    print('')

    output_file = open("referencefiles/bpetrainingoutput.txt", "w") # Create output file to save the printed output to a file

    # Now, use our data to figure out which merges we should make
    while len(ranks) < vocab_size:
        # Find the most common pair. This will become our next token
        stats = collections.Counter()
        for piece in words:
            for pair in zip(piece[:-1], piece[1:]):
                stats[pair] += 1

        most_common_pair = max(stats, key=lambda x: stats[x])
        token_bytes = most_common_pair[0] + most_common_pair[1]
        token = len(ranks)
        # Add the new token!
        ranks[token_bytes] = token

        # Now merge that most common pair in all the words. That is, update our training data
        # to reflect our decision to make that pair into a new token.
        new_words = []
        for word in words:
            new_word = []
            i = 0
            while i < len(word) - 1:
                if (word[i], word[i + 1]) == most_common_pair:
                    # We found our pair! Merge it
                    new_word.append(token_bytes)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            if i == len(word) - 1:
                new_word.append(word[i])
            new_words.append(new_word)
        words = new_words

        output_file.write(f"The current most common pair is {most_common_pair[0]} + {most_common_pair[1]}\n") # save printed output to file
        output_file.write(f"So we made {token_bytes} our {len(ranks)}th token\n") # save printed output to file
        output_file.write("Now the first fifty words in our training data look like:\n") # save printed output to file
        output_file.write(str([token for word in words[:50] for token in word])) # save printed output to file
        output_file.write("\n\n") # save printed output to file

        # See the intermediate merges play out!
        if visualise:
            print(f"The current most common pair is {most_common_pair[0]} + {most_common_pair[1]}")
            print(f"So we made {token_bytes} our {len(ranks)}th token")
            if visualise in ["colour", "color"]:
                print("Now the first fifty words in our training data look like:")
                visualise_tokens([token for word in words[:50] for token in word])
            elif visualise == "simple":
                print("Now the first twenty words in our training data look like:")
                for word in words[:20]:
                    print(word)
            # print("\n")
        # print("Finished BPE dictionary training.\n")

    return ranks

def visualise_tokens(token_values: list[bytes]) -> None:
    backgrounds = itertools.cycle(
        [f"\u001b[48;5;{i}m".encode() for i in [167, 179, 185, 77, 80, 68, 134]]
    )
    interleaved = itertools.chain.from_iterable(zip(backgrounds, token_values))
    try:
        print((b"".join(interleaved) + "\u001b[0m".encode()).decode("utf-8"))  
    except UnicodeDecodeError:
        print(interleaved) ## handle multibyte characters

def train_simple_encoding():
    gpt2_pattern = (
        r"""'s|'t|'re|'ve|'m|'ll|'d| ?[\p{L}]+| ?[\p{N}]+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )

    print("This is the training data we will use to train our BPE dictionary:  bpesample.txt.  It's a text  file containing words with only the letters a, b, c, d, e, f, g, h.  After it finishes training, you can test it by encoding a string. \n")

    with open("bpesample.txt", "r") as f:  # put any sample text here to use as source of training data
        # with open(__file__, "r") as f: ## original _educational.py #uses this python script file as source of training data
        data = f.read()

    enc = SimpleBytePairEncoding.train(data, vocab_size=300, pat_str=gpt2_pattern)
    # enc = SimpleBytePairEncoding.train(data, vocab_size=600, pat_str=gpt2_pattern)  #original tiktoken _educational.py

    user_input = input("Please enter a string (we will use the dictionary from the last step to encode it).\n" )
    tokens = enc.encode(user_input)  # original _educational.py
    # print("This is the sequence of merges performed in order to encode 'hello world':")  # original _educational.py
    # tokens = enc.encode("hello world")  # original _educational.py
    # assert enc.decode(tokens) == "hello world"  # original _educational.py
    # assert enc.decode_bytes(tokens) == b"hello world"  # original _educational.py
    # assert enc.decode_tokens_bytes(tokens) == [b"hello", b" world"]  # original _educational.py

    return enc

## Added command line interface...
while True:
    user_input = input("Please enter a string (or 'train' to train, 'q' to quit): \n")
    if user_input.lower() in ['quit', 'q']:
        print("Goodbye!")
        break
    if user_input.lower() in ['train', 't']:
        # Train a new encoder
        print("  In this example, we're using an essay composed of only letters from a to h as our source text.  This means the BPE encoder will not be able to merge characters that come after h in the alphabet.\n"); 
        print("Training a new encoder...")
        print("  The first step is using BPE training to create a dictionary called mergeable_ranks"); time.sleep(1) # print steps
        print("  The next step is using that new dictionary to encode a string\n"); time.sleep(1) # print steps
        enc = train_simple_encoding()
        #    def train(training_data: str, vocab_size: int, pat_str: str):

    else:
        # Visualise how the GPT-4 encoder encodes text
        print("Encoding your input with the GPT-4 encoder...")
        enc = SimpleBytePairEncoding.from_tiktoken("cl100k_base")
        enc.encode(user_input, visualise="colour")
