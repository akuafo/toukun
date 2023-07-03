# open ai cookbook:  How_to_call_functions_with_chat_models.ipynb (part 1)
  # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
  # modified to run in ec2 instead of jupyter notebook

import arxiv
import ast
import concurrent
from csv import writer
#from IPython.display import display, Markdown, Latex
import json
import openai
import os
import pandas as pd
from PyPDF2 import PdfReader
import requests
from scipy import spatial
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken
from tqdm import tqdm
from termcolor import colored

GPT_MODEL = "gpt-3.5-turbo-0613"
EMBEDDING_MODEL = "text-embedding-ada-002"

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    try:
        #print(headers)
        #print(json_data)
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        #print the request parameters
        print("request parameters:")
        print(response.request.body)
        #print the response body
        print("response body:")
        print(response.text)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    
class Conversation:
    def __init__(self):
        self.conversation_history = []

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)

    def display_conversation(self, detailed=False):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        for message in self.conversation_history:
            print(
                colored(
                    f"{message['role']}: {message['content']}\n\n",
                    role_to_color[message["role"]],
                )
            )

functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
            },
            "required": ["location", "format"],
        },
    }
]

conversation = Conversation()
#conversation.add_message("user", "what is the weather like today") # this was the prompt in the jupyter notebook

#prompt user on the command line
user_input = input("Type the user prompt.")
conversation.add_message("user", user_input)

# The model first prompts the user for the information it needs to use the weather function
chat_response = chat_completion_request(
    conversation.conversation_history, functions=functions
)
# assistant_message = chat_response.json()["choices"][0]["message"]
# conversation.add_message(assistant_message["role"], assistant_message["content"])
#assistant_message # this was the prompt in the jupyter notebook

#display output on the command line
# print(str(assistant_message))

# # OUTPUT:
# # {'role': 'assistant',
# # 'content': 'Sure, can you please provide me with your location or the city you want to know the weather for?'}

# # Once the user provides the required information, the model can generate the function arguments
# conversation.add_message("user", "I'm in Glasgow, Scotland")
# chat_response = chat_completion_request(
#     conversation.conversation_history, functions=functions
# )
# chat_response.json()["choices"][0]

# # OUTPUT:
# # {'index': 0,
# #  'message': {'role': 'assistant',
# #   'content': None,
# #   'function_call': {'name': 'get_current_weather',
# #    'arguments': '{\n  "location": "Glasgow, Scotland",\n  "format": "celsius"\n}'}},
# #  'finish_reason': 'function_call'}

