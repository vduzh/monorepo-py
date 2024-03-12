import json
import unittest
from pprint import pprint

from libs.openai.model import get_llm, get_model_name, get_embedding_model_name


class TestOpenAI(unittest.TestCase):
    def setUp(self):
        self.client = get_llm()

    def test_create_completion(self):
        test_value = "This is a test!"
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Say " + test_value}
            ],
            model=get_model_name(),
        )
        # pprint(chat_completion)

        self.assertEqual(1, len(chat_completion.choices))

        choice = chat_completion.choices[0]
        self.assertEqual('stop', choice.finish_reason)

        message = choice.message
        self.assertEqual(test_value, message.content)
        self.assertEqual("assistant", message.role)

    def test_create_completion_with_2_choices(self):
        test_value = "This is a test!"
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Say " + test_value}
            ],
            model=get_model_name(),
            n=2
        )
        # pprint(chat_completion)

        self.assertEqual(2, len(chat_completion.choices))

    def test_function_calling(self):
        model_name = get_model_name()

        # Example dummy function hard coded to return the same weather
        def get_current_weather(location, unit="fahrenheit"):
            """Get the current weather in a given location"""
            if "minsk" in location.lower():
                return json.dumps({"location": "Minsk", "temperature": "6", "unit": unit})
            elif "warsaw" in location.lower():
                return json.dumps({"location": "Warsaw", "temperature": "10", "unit": unit})
            else:
                return json.dumps({"location": location, "temperature": "unknown"})

        # Run conversation
        # Step 1: send the conversation and available functions to the model
        messages = [
            {
                "role": "user",
                "content": "What's the weather like in Minsk and Warsaw?"
            }
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city, e.g. Milan",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )

        response_message = response.choices[0].message

        tool_calls = response_message.tool_calls

        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors

            # only one function in this example, but you can have multiple
            available_functions = {
                "get_current_weather": get_current_weather,
            }

            # extend conversation with assistant's reply
            messages.append(response_message)

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )

                # extend conversation with function response
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

            # get a new response from the model where it can see the function response
            second_response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
            )

            print("Result:", second_response.choices[0].message.content)

    def test_create_embedding(self):
        test_text = "This is a test!"
        res = self.client.embeddings.create(
            input=test_text,
            model=get_embedding_model_name(),
        )

        embedding = res.data[0].embedding
        pprint(embedding[:10])

        self.assertTrue(len(embedding) > 0)


if __name__ == '__main__':
    unittest.main()
