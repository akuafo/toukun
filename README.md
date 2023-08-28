# An exploration of OpenAI tokenization (tiktoken _educational and more)

This is a work-in-progress walkthrough of the OpenAI tiktoken package including Python examples of text tokenization, viewing the internal dictionary, multi-byte unicode, logit bias, and more.  The scripts in this repository were created for learning and experimentation.

To get started, follow these steps from the terminal command line:
- Clone this project: git clone https://github.com/akuafo/toukun.git
- Navigate into the directory: cd toukun
- Install the tiktoken package from OpenAI:  pip install tiktoken
- Open the terminal and run the scripts listed below

Table of contents:
- <a href="#Background">Tokenization and Tiktoken
- <a href="#Text-to-token">Tiktoken text to token (encode/decode)
- <a href="#Train-BPE">Train a new BPE (modified Tiktoken _educational.py)
- <a href="#Counting-tokens">Tiktoken for counting tokens
- <a href="#Logit-bias">Adding tokens to logit bias to influence chat completions
- <a href="#Dictionary-files">Save the internal tiktoken dictionary as bytes and utf-8
- <a href="#Special-tokens">Special tokens
- <a href="#Tiktoken-regex">The Tiktoken regex for initial splitting of text

![Screenshot of command line](https://github.com/akuafo/toukun/blob/main/commandline.jpg)

## <a id="Background"></a>Tokenization and Tiktoken

This is an educational walkthrough of OpenAI's Tiktoken, a Python library developed by OpenAI that converts text to tokens.

Tokenization involves breaking down text into small numerical tokens that machine learning models can process. These tokens might represent individual characters or they could be words or phrases.  Tiktoken uses a type of tokenization known as Byte Pair Encoding (BPE) which starts with a base vocabulary of individual characters and iteratively merges the most common pair of consecutive characters to form new tokens.

Knowing how many tokens are in a text string can tell you (a) whether the string is too long for a text model to process and (b) how much an OpenAI API call costs (as usage is priced by token).  It also lets you customize the logit bias to influence chat completions.

For these samples, the tiktoken model is 'cl100k_base model' since that is the model used for GPT-4.  You set the model when you instantiate an encoding object:  encoding = tiktoken.get_encoding("cl100k_base").  The list of models are stored at tiktoken/tiktoken/model.py.

## <a id="Text-to-token"></a>Tiktoken's core text encoding and decoding functions

### Converting from text to token, from token to text

At the command line, run this script:

    python3 encodedecode.py

This script will run an interactive session from the command line to convert tokens and text via Tiktoken.  It gives you two options:  enter a string of text and see the tokens, or enter a token and see the text.  You can try multi-byte unicode characters too.

For example, here is a sample session:

    Please enter a command: 
    ('s' to input string, 't' to input token', or 'q' to quit) 
    s
    Enter a string to encode: ok
    Titoken results:
    array of tokens of length 1
        token as integer: 564 | token as string: ok | token as byte literal: b'ok'

    Please enter a command: 
    ('s' to input string, 't' to input token', or 'q' to quit) 
    s
    Enter a string to encode: okok
    Titoken results:
    array of tokens of length 2
        token as integer: 564 | token as string: ok | token as byte literal: b'ok'
        token as integer: 564 | token as string: ok | token as byte literal: b'ok'

    Please enter a command: 
    ('s' to input string, 't' to input token', or 'q' to quit) 
    t
    Enter a token to decode (integer: 100
    Titoken results:
    array value: [100] | decode to string: � | decode to byte literal: b'\xa7'

    Please enter a command: 
    ('s' to input string, 't' to input token', or 'q' to quit) 
    q


## <a id="Train-BPE"></a>Train a new BPE

### Tiktoken _educational.py

Here is a modified version of _educational.py that runs from the command line and prints out more detail.  Tiktoken's own _educational.py is very helpful for understanding concepts, but I found it fairly difficult to understand the first time through.  Thus this script breaks down the steps a little more.

Run this script:

    python3 tiktoken_educational.py

Enter a text string and watch the process by which the string is split and then merged back together into tokens.

Next, choose the 'train' option.  This will train based on a text file with limited letters of a to h.  It will generate a new BPE dictionary.  Then it will take a sample string and split and merge it using the new dictionary.

In this example, the source text for building the BPE dictionary is a ChatGPT-generated essay composed of only letters from 'a' to 'h'.  This means the BPE encoder will not be able to merge characters that come after 'h' in the alphabet.

Now, try entering the same text string again, and observe that it can't do merges for the letters that aren't in the dictionary.

## <a id="Counting-tokens"></a>Tiktoken for counting tokens

### Convert text to tokens and count them

Counting tokens is the most common use case for using Tiktoken.  It's used to ensure that input will fit within the context window and also to estimate OpenAI costs which are priced per token.

Install the OpenAI Python package 'openai' to use the OpenAI API:

    pip install openai

You'll need to setup an OpenAI developer account.  Then, add your developer key as an environment variable.
Linux/Mac:  
    export OPENAI_KEY=your_key
Windows:  
    set OPENAI_KEY=your_key)

Run this script:

    python3 counttokens.py

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

## <a id="Dictionary-files"></a>View tiktoken dictionary as bytes and utf-8 strings

This python script will write out several files in different formats to help to understand the tiktoken dictionary, encoding, and parsing.

The files are saved to the directory 'referencefiles'.

From the terminal, run this script.

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

## <a id="Special-tokens"></a>Special tokens

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

## <a id="Tiktoken-regex"></a>The Tiktoken regex for initial splitting of text

### Regex
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

To observe more about how the tiktoken regex works, you can run _educational.py script.
