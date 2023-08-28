# features/encodedecode.feature

Feature: TikToken Encoding and Decoding
  As a user, I want to encode and decode strings and tokens so that I can understand their representations.

  # Existing Scenarios
  # ...

  Scenario Outline: Encoding specific strings
    Given the user input string "<input_string>"
    When the string is encoded
    Then the token results should have length <expected_length>

    Examples:
      | input_string | expected_length |
      | a            | 1               |
      | hello, world | 3              |
      | 日           | 1               |

