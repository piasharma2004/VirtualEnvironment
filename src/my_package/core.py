import os
import json
from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ],
    temperature=0.7,
    max_tokens=150
)

# Print the response
print("Response content:")
print(response.choices[0].message.content)

# Let's explore the response object
print("\\nType of response object:", type(response))
print("\\nAvailable attributes and methods:")
for attr in dir(response):
    if not attr.startswith('_'):  # Skip internal attributes
        print(f"- {attr}")

# Look at the full response (serialized to dictionary)
print("\\nFull response as dictionary:")
response_dict = response.model_dump()
print(json.dumps(response_dict, indent=2))

def main():
    print("Hello from virtualenvironment!")


if __name__ == "__main__":
    main()
