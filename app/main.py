"""Main application file."""

import argparse
import os
import sys
import json

from openai import OpenAI

from app.tools import read_file

# Load configuration from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
MOODEL = os.getenv("OPENROUTER_MODEL", default="anthropic/claude-haiku-4.5")
# Tools registry and metadata for the model to know how to call them
TOOLS_REGISTRY = {"read_file": read_file}
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        },
    }
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # Initialize conversation history
    messages = [{"role": "user", "content": args.p}]

    # Agent loop
    while True:
        chat = client.chat.completions.create(
            model=MOODEL,
            messages=messages,
            tools=TOOLS,
            max_tokens=4000,
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        message = chat.choices[0].message

        # Append assistant's response to conversation history
        messages.append(message)

        # Check if the model wants to use tools
        if not message.tool_calls:
            # No tool calls - final response, print and exit
            print(message.content)
            break

        # Execute each tool call and add results to messages
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                print(f"Unknown tool call type: {tool_call.type}", file=sys.stderr)
                continue

            tool = TOOLS_REGISTRY[tool_call.function.name]
            result = tool(**json.loads(tool_call.function.arguments))
            print(
                f"Tool call: {tool_call.function.name}({tool_call.function.arguments}) -> {result}",
                file=sys.stderr,
            )

            # Add tool result to conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


if __name__ == "__main__":
    main()
