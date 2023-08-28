# features/steps/encodedecode_steps.py

from behave import given, when, then
from encodedecodemodule import encode_string, decode_token  # I'm assuming these functions exist in your encodedecodemodule.py

@given('the user input string "{input_string}"')
def step_impl(context, input_string):
    context.input_string = input_string

@when('the string is encoded')
def step_impl(context):
    context.encoded_result = encode_string(context.input_string)  # assuming your function returns a list of tokens

@then('the token results should have length {expected_length}')
def step_impl(context, expected_length):
    assert len(context.encoded_result) == int(expected_length), f"Expected length {expected_length}, but got {len(context.encoded_result)}"
