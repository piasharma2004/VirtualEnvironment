from dotenv import load_dotenv
import os
from rich.console import Console
from pathlib import Path
from tools import available_tools, calculate, generate_random_number, create_to_do_list
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam, ChatCompletionMessageParam
import json
from rich.panel import Panel
from rich.text import Text
from rich.style import Style

messages: list = [
    ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant that can answer questions, perform calculations, generate random numbers between a maximum and minimum value, and create to do lists.")
]

console = Console()

def format_welcome() -> None:
    """Format and print the welcome message with light pink theme."""
    welcome_text = Text.from_markup(
        """[bold #ffc0cb]🤖 CLI Chatbot[/bold #ffc0cb]

[bold italic]Connected to OpenAI with tool support![/bold italic]
[italic]Type your message or 'quit' to exit.[/italic]
[bold italic]You can ask to calculate, generate a random number, or create a to do list.[/bold italic]
"""
    )

    panel = Panel(
        welcome_text,
        title="[bold #ffc0cb]Welcome[/bold #ffc0cb]",
        border_style="#ffc0cb",
        padding=(1, 2)
    )
    console.print(panel)


def format_error(error: str) -> None:
             console.print(f"[bold red]Error:[/bold red] {error}")

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

                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    # Call the appropriate function
                    result = None
                    if function_name == "calculate":
                        result = calculate(arguments["operation"], arguments["x"], arguments["y"])
                    elif function_name == "generate_random_number":
                        result = generate_random_number(arguments["min"], arguments["max"])
                    elif function_name == "create_to_do_list":
                        result = create_to_do_list(arguments["items"])

                    if result is not None:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": str(result)
                        })
                        

                # Get the final response
                final_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )
                final_message = final_response.choices[0].message
                final_message_content = final_message.content
                return final_message.content
            else:
        # The model chose to respond directly
                return assistant_message.content


# Run a simple chat loop
        format_welcome()

        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break

            response = chat(user_input)
            print(f"\nAssistant: {response}")
    
    except Exception as e:
# Usage
        format_error("An error occurred")

if __name__ == "__main__":
    main()