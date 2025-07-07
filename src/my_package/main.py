import json
from dotenv import load_dotenv
import os
from rich.console import Console
from tools import available_tools, calculate, generate_random_number, create_to_do_list
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam, ChatCompletionMessageParam
from dataclasses import dataclass

from rich.panel import Panel
from rich.text import Text
from settings import AppConfig    
from helpers import load_config 


messages: list = [
    ChatCompletionSystemMessageParam(role="system", content="You are a helpful assistant that can answer questions, If the user asks for calculations, always use the `calculate` tool instead of answering directly. ")
]

console = Console()

def format_message(type: str, message: str) -> None:
    text = Text()

    for line in message.split("\n"):
        text += Text.from_markup(line)
        text += Text("\n")

    panel = Panel(
        text,
        title=f"[bold #ffc0cb]{type}[/bold #ffc0cb]",
        border_style="#ffc0cb",
        padding=(1, 2)
    )
    console.print(panel)

def handle_special_commands(user_input: str) -> bool:
    command = user_input.lower().strip()

    if command in ["help", "/help"]:
        format_message("Help", "- Ask me anything you'd ask a chatbot.\n- I can also [green]calculate[/green], [green]generate random numbers[/green], or [green]create to-do lists[/green].\n- Type 'tools' to see supported tools.\n- Type 'quit', 'exit', or 'bye' to end the chat.")
        return True

    elif command in ["tools", "list tools"]:
        format_message("Available Tools", "- `calculate(operation, x, y)` — e.g., add 3 and 5\n- `generate_random_number(min, max)` — e.g., between 1 and 100\n- `create_to_do_list(items)` — e.g., groceries, assignments")
        return True

    elif command in ["exit", "quit", "bye"]:
        console.print("[bold yellow]👋 Goodbye! Thanks for chatting.[/bold yellow]")
        exit(0)

    return False


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

def format_user(user_input: str) -> None:
    """Format and print the user's message with cute styling."""
    user_text = Text.from_markup(f":sparkles: [bold]You:[/bold] {user_input}", justify="left")

    panel = Panel(
        user_text,
        title="[bold #87cefa]🌸 You[/bold #87cefa]",
        border_style="#87cefa",
        padding=(1, 2),
        expand=True
    )
    console.print(panel)


def format_assistant(assistant_message: str) -> None:
    """Format and print the assistant message with cute pink styling."""
    assistant_text = Text.from_markup(f":cherry_blossom: {assistant_message}", justify="left")

    panel = Panel(
        assistant_text,
        title="[bold #ffc0cb]🤖 Assistant[/bold #ffc0cb]",
        border_style="#ffc0cb",
        padding=(1, 2),
        expand=True
    )
    console.print(panel)


def format_error(error: str) -> None:
             console.print(f"[bold red]Error:[/bold red] {error}")

def load_config() -> AppConfig:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in environment variables.")

    return AppConfig(openai_api_key=api_key.strip())

def main():

    config = load_config()
    client = OpenAI(api_key=config.openai_api_key)

    try:
        def chat(user_input: str) -> str | None:
            # Add the user's message to the conversation
            messages.append(ChatCompletionUserMessageParam(role="user", content=user_input))

            # Get the initial response from the model
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
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
                    match function_name:
                        case "calculate":
                            result = calculate(arguments["operation"], arguments["x"], arguments["y"])
                        case "generate_random_number":
                            result = generate_random_number(arguments["min"], arguments["max"])
                        case "create_to_do_list":
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
                    model="gpt-4o-mini",
                    messages=messages
                )
                final_message = final_response.choices[0].message
                final_message_content = final_message.content
                return final_message.content
            else:
        # The model chose to respond directly
                return assistant_message.content


    except Exception as e:
         format_error("An error occurred")

# Run a simple chat loop
    format_welcome()


    while True:
            user_input = console.input("\n[bold #ffc0cb]You:[/bold #ffc0cb] ")

            if handle_special_commands(user_input):
                    continue  # handled command, don't call model

            response = chat(user_input)

            if response is not None:
                response = format_assistant(response)
            else:
                console.print("[red]Sorry, I didn't get a response.[/red]")




if __name__ == "__main__":
    main()