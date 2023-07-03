# Compare logit bias across multiple OpenAI models
#https://colab.research.google.com/drive/1fx0NeWHE7S97gdvadR-WC0z36R2Z_mu9

from prettytable import PrettyTable
import time
import openai
import tiktoken

# Function to get token IDs for a given model family
def get_token_ids(model_family, text):
    if 'gpt-4' in model_family:
        model_enc = tiktoken.encoding_for_model("gpt-4")
    else:
        model_enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return model_enc.encode(text)

# here we're doing happy, sad, neutral sentiment analysis... feel free to adjust for your use-case
test_cases = [
    {
        'input': 'My name is Matt',
        'expected_output': 'neutral'
    },
    {
        'input': 'I am so happy today!',
        'expected_output': 'happy'
    },
    {
        'input': 'I had a bad day.',
        'expected_output': 'sad'
    },
    {
        'input': 'The temperature is 50 degrees.',
        'expected_output': 'neutral'
    },
    {
        'input': 'I just won the lottery!',
        'expected_output': 'happy'
    }
]

models = ['gpt-4', 'gpt-4-0613', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo'] # choose what models you'd like to benchmark
model_results = {model: {'correct': 0, 'total': 0} for model in models}

# Initialize the table
table = PrettyTable()
table.field_names = ["Input", "Expected"] + models

# Wrap the text in the "Input" column
table.max_width["Input"] = 100

# Initialize timers
model_timers = {model: 0 for model in models}

for test_case in test_cases:

    row = [test_case['input'], test_case['expected_output']]

    for model in models:

        logit_bias_values = {
            'happy': get_token_ids(models[0], 'happy')[0],
            'sad': get_token_ids(models[0], 'sad')[0],
            'neutral': get_token_ids(models[0], 'neutral')[0]
        }

        start_time = time.time()

        x = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": "Determine the sentiment of the input statement. Return 'happy', 'sad', or 'neutral'."}, # adjust for your use-case
                {"role": "user", "content": f"Here is the statement: `{test_case['input']}`"} # adjust for your use-case
            ],
            logit_bias={
                str(logit_bias_values['happy']): 100,
                str(logit_bias_values['sad']): 100,
                str(logit_bias_values['neutral']): 100
            },
            max_tokens=1,
            temperature=0,
        ).choices[0].message.content

        end_time = time.time()
        model_timers[model] += (end_time - start_time)

        status = "✅" if x == test_case['expected_output'] else "❌"
        row.append(status)

        # Update model results
        if x == test_case['expected_output']:
            model_results[model]['correct'] += 1
        model_results[model]['total'] += 1

    table.add_row(row)

print(table)

# Calculate and print the percentage of correct answers and average time for each model
for model in models:
    correct = model_results[model]['correct']
    total = model_results[model]['total']
    percentage = (correct / total) * 100
    avg_time = model_timers[model] / total
    print(f"{model} got {percentage:.2f}% correct. Average time: {avg_time:.2f} seconds.")