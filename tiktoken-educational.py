import time  # import the time module

from tiktoken._educational import *  

# Train a BPE tokeniser on a small amount of text
#print("starting test python file...")
#time.sleep(1.5)  # add delay here

#enc = train_simple_encoding()

# Visualise how the GPT-4 encoder encodes text
#enc = SimpleBytePairEncoding.from_tiktoken("cl100k_base")
#enc.encode("hello world aaaaaaaaaaaa")

# moved this code into the package code so that I don't have to reinstall the package to call it.  I can call it directly:
#        python3 tiktoken-main/tiktoken/_educational.py