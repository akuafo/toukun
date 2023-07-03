# Toukun - tokenization and AI

A tutorial for understanding the OpenAI tiktoken package and more generally how text is input into the AI model.

Prerequisite:
* A Python environment

Getting started:
* clone this project
* cd toukun
* pip install -e . (this will install this project with openai's tiktoken as a submodule as an editable package so you can change the source code)

Table of Contents:
- <a href="#Background">Brief background on tokenization
- <a href="#Dicionary-files">View tiktoken dictionary as bytes and utf-8 strings
- <a href="#section1">Converting from text to token and back again
- <a href="#section1">Segmentation of the string
- <a href="#section1">Tokenization of the segments
- <a href="#section1">Merging of the segments
- <a href="#section1">Special tokens
- <a href="#section1">Base64 and unicode
- <a href="#section1">Non-English languages
- <a href="#section1">Quirks and weirdness
- <a href="#section1">Using tokenization with the OpenAI API
- <a href="#section1">Appendix:  Training your own BPE

## <a id="Background"></a>Brief background on tokenization and tiktoken

Tokenization involves breaking down text into smaller units, known as tokens, in a structured numerical format which machine learning models can process. These tokens may be individual characters, subwords, words, or phrases.

OpenAI uses a specific type of tokenization known as Byte Pair Encoding (BPE) which starts with a base vocabulary of individual characters and iteratively merges the most common pair of consecutive characters to form new tokens. This process continues until a desired vocabulary size is reached. BPE strikes a balance between character-level tokenization, which can handle any word but doesn't capture any word structure, and word-level tokenization, which can capture word structure but can't handle out-of-vocabulary words.

Tiktoken is a Python library developed by OpenAI that allows you to count the number of tokens in a text string according to OpenAI's tokenization rules, without making an API call. This can be useful for understanding how much text will fit within the context limit and for estimating costs.

It also provides a window into how the AI model accepts the input of text.  The AI model is a black box, but tiktoken allows you to see how the text is converted into tokens and how the tokens are converted back into text.

## <a id="OpenAI Models"></a>Tiktoken support for various OpenAI models

Note:  Throughout these exercises, we'll set the tiktoken model as 'cl100k_base model' since that is the most recent model and is used for GPT-4.  While there are variations in how tiktoken performs tokenization with the different models, the basic concepts are the same.

In tiktoken, you set the model when you instaniate an encoding object:

    encoding = tiktoken.get_encoding("cl100k_base")  # Using the cl100k_base model.

The list of models are stored in the model.py file in tiktoken:
    tiktoken/tiktoken/model.py

## <a id="Dictionary-files"></a>View tiktoken dictionary as bytes and utf-8 strings

This python script will write out several files in different formats to help to understand the tiktoken dictionary, encoding, and parsing.

The files are saved to the directory 'referencefiles'.

Run this script.

    python3 outputfiles.py

This script will output the following files:

    # File:  
      referencefiles/cl100k_base.tiktoken

    This file consists of the dictionary of base64 encoded tokens and their index numbers.
    The source file is at this URL:  https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken

    # Files:
      referencefiles/cl100k_base_byteliterals.txt
      referencefiles/cl100k_base_utf8.txt
    
    This step will convert the text-related values in the cl100k_base file and output two additional files.

    For the first output file, we'll be decoding the bash64 values which will result in byte literals.  
    For example, the letter A becomes the string literal b'A'.

    For the second output file, we'll decode the base64 values into UTF-8 strings so that we can see double-byte characters.
        For example, character 22656 is the byte literal b'\xe6\x9c\xac' which corresponds to the Japanese kanji 本.
        Sometimes the bytes are not valid UTF-8 so it substitutes the default 'replace' unicode character.
        Sometimes there will be formatting characters like carriage returns that will display weirdness in a text editor.
        cl100k_base_byteliterals.txt and cl100k_base_utf8.txt have been written successfully.

### Converting from text to token, from token to text

Run this script.

    python3 encodedecode.py

This script will run an interactive session from the command line to convert tokens and text via Tiktoken.  You have two options:  enter a string of text and see the tokens, or enter a token and see the text.

### Segmenting and merging

The first step in BPE tokenization is to split the input string into individual tokens.  The regex used to split strings in tiktoken can be retrieved through the encoding object:

    encoding._pat_str

The actual regex string is the following:

    (?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+

It's pretty complex because it has to handle any type of text in any language including meaningless and machine generated text.

The regex logic handles the following (and more):
- contractions like don't and I'm
- Unicode letter characters which may be preceded by non-letter, non-number characters
- Number characters
- Newline or carriage return characters
- Spaces of varying lengths

The string is split into individual segments and then progressively merged into larger segments based on which tokens have the higher rank.

Try this code...
    print("\n  Fun with regex...") # from _educational.py, need to import regex to run it
    regex.compile(encoding._pat_str)
    words = self._pat.findall(user_input)     # Use the regex to split the text into (approximately) words

### Special tokens

These can be seen in the encoding object in core.py:

encoding._special_tokens
{'<|endoftext|>': 100257,
'<|fim_prefix|>': 100258,
'<|fim_middle|>': 100259,
'<|fim_suffix|>': 100260,
'<|endofprompt|>': 100276}

in the tiktoknen readme and 
"<|im_start|>": 100264
"<|im_end|>": 100265

from vercel app
<|im_start|>
<|im_sep|>
<|im_end|>

Documentation from openapi API reference...
'role' is the messages author. One of system, user, assistant, or function.
'messages' is a list of messages comprising the conversation 
'content' is the contents of the message and is required for all messages except assistant messages with function calls
The name of the author of this message. name is required if role is function, 
Example API request from docs:
{
  "model": "gpt-3.5-turbo",
  "messages": 
     [{
      "role": "system", 
      "content": "You are a helpful assistant." 
     },
     {
      "role": "user", 
      "content": "Hello!"
     }]
}

Hierachy of a typical chatgpt api request (excluding functions):
Request body:  json object
Array of json objects ('messages')
json objects:  two key/value pairs
key/value pairs:  role, content

### Counting tokens

counttokens.py
This is an expanded version of the example in the openai cookbook it so we can see in more detail the text being passed back and forth int the chat conversation, and calculate the tokens based on that.

### Experiments with the OpenAI API

Run this script:
    python3 logitbiastokens.py

This script will query the OpenAI chat API along with logit bias parameters at maximum setting.  The logit bias is a measure of how likely the token is to be used in the next word of the conversation.  The higher the logit bias, the more likely the token will be used.  This will force the OpenAI response to respond with these tokens.

    In this exercise, we will create a logitbias dictionary to force the OpenAI API to respond with a specific output."
    The challenge is encapsulating your intended logic in a single 'word' that's in the tiktoken dictionary."
    For a simple example, try 'true' and false' along with the test queries of 'does 2 + 2 = 4' and 'does 2 + 2 = 5'"
    Please enter a word for your logit bias, and we will try to encode it as a token.

Inspired by these posts:
        https://twitter.com/AAAzzam/status/1669753722828730378/photo/1
        https://www.factsmachine.ai/p/the-prodigal-json
        https://twitter.com/QVagabond/status/1669759115252445191

### Non-English languages, non-human languages, and random high priority word fragments in Tiktoken

### More resources:
- Training your own BPE (see example in _educationals.py)
