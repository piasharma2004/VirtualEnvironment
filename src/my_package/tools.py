import random


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

def generate_random_number(min, max):
    """Generate a random number between min and max."""
    return random.randint(min, max)

def create_to_do_list(items):
    """Create a to do list."""
    return "\n".join(f"- {item}" for item in items)
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
    }, {
        "type": "function",
        "function": {
            "name": "generate_random_number",
            "description": "Generate a random number between a minimum and maximum value",
            "parameters": {
                "type": "object",
                "properties": {
                    "min": {
                        "type": "number",
                        "description": "The minimum value"
                    },
                    "max": {
                        "type": "number",
                        "description": "The maximum value"
                    }
                },
                "required": ["min", "max"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_to_do_list",
            "description": "Create a to do list",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The list of items to include in the to do list"
            }
    },
                "required": ["items"]
            }
        }
    }
]
