from dotenv import load_dotenv
import os
from pathlib import Path
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam, ChatCompletionMessageParam
import json

messages: list = [
    ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant that can answer questions, perform calculations, tell jokes, and create to do lists.")
]

def calculate(operation, x, y):
    """Perform a mathematical operation."""
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        if y == 0:
            return "Error: Division by zero"
        return x / y
    else:
        return f"Error: Unknown operation '{operation}'"

# Define available tools as a LIST of tool specifications
available_tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical operation on two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The mathematical operation to perform"
                    },
                    "x": {
                        "type": "number",
                        "description": "The first number"
                    },
                    "y": {
                        "type": "number",
                        "description": "The second number"
                    }
                },
                "required": ["operation", "x", "y"]
            }
        }
    }
]

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key.strip())

    try:
        def chat(user_input):
            # Add the user's message to the conversation
            messages.append(ChatCompletionUserMessageParam(role="user", content=user_input))

            # Get the initial response from the model
            response = client.chat.completions.create(
                model="gpt-4",  # Changed to valid model name
                messages=messages,
                tools=available_tools,  # Directly pass the list, no .values()
                tool_choice="auto"
            )

            # Get the assistant's message
            assistant_message = response.choices[0].message
            messages.append(assistant_message.model_dump())

            # Check if the model wants to call any functions
            if assistant_message.tool_calls:
                print("Processing function calls...")
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    print(f"Function call: {function_name}({arguments})")

                    # Call the appropriate function
                    result = None
                    if function_name == "calculate":
                        try:
                            result = calculate(arguments["operation"], arguments["x"], arguments["y"])
                        except Exception as e:
                            result = f"Error in calculation: {str(e)}"

                    if result is not None:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": str(result)
                        })
                        print(f"Function result: {result}")

                # Get the final response
                final_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                final_message = final_response.choices[0].message
                messages.append(final_message.model_dump())
                return final_message.content
            else:
                return assistant_message.content

        # Start the conversation
        print("Assistant:", chat("Hello! Can you tell me about yourself?"))
        print("\nAssistant:", chat("What can you help me with?"))
        print("\nAssistant:", chat("Calculate 123 + 456"))  # Test the calculator
        print("\nAssistant:", chat("Tell me a short joke about programming."))

        # Print conversation history
        print("\nFull conversation history:")
        for message in messages:
            role = message["role"].capitalize()
            content = message["content"]
            print(f"{role}: {content}\n")

    except Exception as e:
        print(f"\nError making API request: {e}")

if __name__ == "__main__":
    main()