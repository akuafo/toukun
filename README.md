# An exploration of OpenAI tokenization (tiktoken _educational and more)

This is a walkthrough of the OpenAI tiktoken package including Python examples of text tokenization, viewing the internal dictionary, multi-byte unicode, logit bias, and more.  The scripts in this repository were created for learning and experimentation.

Getting started:
* clone this project
* cd toukun
* pip install . (this will install this project with openai's tiktoken as a submodule)
    editable package so you can change the source code

Table of Contents:
- <a href="#Background">Brief background on tokenization
- <a href="#OpenAI-models">Choosing the OpenAI models for tokenization
- <a href="#Dicionary-files">Save the internal tiktoken dictionary as bytes and utf-8
- <a href="#Text-to-token">Tiktoken's core text encoding and decoding functions
- <a href="#Tiktoken-regex">The Tiktoken regex for initial splitting of text
- <a href="#Counting-tokens">Tiktoken for counting tokens
- <a href="#section1">Merging of the segments
- <a href="#Logit-bias">Adding tokens to logit bias to influence chat completions
- <a href="#More-resources">More resources

## <a id="Background"></a>Background

This is an educational walkthrough of OpenAI's Tiktoken, a Python library developed by OpenAI to convert text to tokens for their API.

In a general sense, tokenization involves breaking down text into small numerical 'tokens' that machine learning models to process. These tokens might represent individual characters or they could be words or phrases.  Tiktoken uses a type of tokenization known as Byte Pair Encoding (BPE) which starts with a base vocabulary of individual characters and iteratively merges the most common pair of consecutive characters to form new tokens.

Knowing how many tokens are in a text string can tell you (a) whether the string is too long for a text model to process and (b) how much an OpenAI API call costs (as usage is priced by token).

Some real world use cases for Tiktoken  include counting the number of tokens that can fit within the chat context window, estimating OpenAI license costs which are per token, customizing the logit bias to influence chat completions, and passing tokens as input to the embeddings API.

## <a id="OpenAI-models"></a>Tiktoken support for OpenAI models

Note:  Throughout these exercises, we'll set the tiktoken model as 'cl100k_base model' since that is the most recent model and is used for GPT-4.  While there are variations in how tiktoken performs tokenization with the different models, the basic concepts are the same.

In tiktoken, you set the model when you instantiate an encoding object:

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

## <a id="Text-to-token"></a>Tiktoken's core text encoding and decoding functions

### Converting from text to token, from token to text

Run this script.

    python3 encodedecode.py

This script will run an interactive session from the command line to convert tokens and text via Tiktoken.  It gives you two options:  enter a string of text and see the tokens, or enter a token and see the text.

## <a id="Tiktoken-regex"></a>The Tiktoken regex for initial splitting of text

### Regex

To see the tiktoken regex in action, you can try the below script which is a modified version of tiktoken's own _educational.py script.

Run this script:

    python3 tiktoken-educational.py

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

## <a id="Counting-tokens"></a>Tiktoken for counting tokens

### Convert text to tokens and count them

Counting tokens is the most common use case for using Tiktoken.  It's used to ensure that input will fit within the context window and also to estimate OpenAI costs which are priced per token.

Run this script:

    counttokens.py

This is an expanded version of the example in the openai cookbook.  This script prints out more detail about the text being passed back and forth in the chat conversation and calculates the tokens based on that.

## <a id="Logit-bias"></a>Adding tokens to logit bias to influence chat completions

### Experiments with logit bias

Run this script:

    python3 logitbiastokens.py

This script will query the OpenAI chat API along with logit bias parameters at maximum setting.  The logit bias is a measure of how likely the token is to be used in the next word of the conversation.  The higher the logit bias, the more likely the token will be used.  This will force the OpenAI response to respond with these tokens.

    In this exercise, we will create a logitbias dictionary to force the OpenAI API to respond with a specific output."
    The challenge is encapsulating your intended logic in a single 'word' that's in the tiktoken dictionary."
    For a simple example, try 'true' and false' along with the test queries of 'does 2 + 2 = 4' and 'does 2 + 2 = 5'"
    Please enter a word for your logit bias, and we will try to encode it as a token.

More on logit bias from these resources:
- https://twitter.com/AAAzzam/status/1669753722828730378/photo/1
- https://www.factsmachine.ai/p/the-prodigal-json
- https://twitter.com/QVagabond/status/1669759115252445191
- https://colab.research.google.com/drive/1fx0NeWHE7S97gdvadR-WC0z36R2Z_mu9

## <a id="More-resources"></a>More resources

### Tiktoken _educational.py

Here is a modified version of _educational.py that runs from the command line and prints out more detail.  Tiktoken's own _educational.py is very helpful for understanding concepts, but I found it fairly difficult to understand the first time through.  Thus this script breaks down the steps a little more.

Run this script:

    python3 tiktoken-educational.py

(Future to do:  Breakdown of creating vocabularies by inputting your own text from 'Training your own BPE' from _educational.py.)

### Special tokens

Special tokens are a very important concept in ChatGPT.  The following special tokens can be found in the encoding object in core.py:

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

### Non-English languages, non-human languages, and random high priority word fragments in Tiktoken

