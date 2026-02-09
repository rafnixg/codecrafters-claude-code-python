"""Main application file."""

import argparse
import os

from openai import OpenAI

from app.agent import Agent
from app.tools import create_default_registry

# Configuration from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
MODEL = os.getenv("OPENROUTER_MODEL", default="anthropic/claude-haiku-4.5")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", required=True, help="Prompt to send to the agent")
    args = parser.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    tools = create_default_registry()
    agent = Agent(client=client, model=MODEL, tools=tools)

    result = agent.run(args.p)
    print(result)


if __name__ == "__main__":
    main()
