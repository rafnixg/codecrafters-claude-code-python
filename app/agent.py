"""Agent class that implements the conversation loop."""

import json
import sys

from openai import OpenAI

from app.tool import ToolRegistry


class Agent:
    """AI Agent that can use tools to accomplish tasks."""

    def __init__(
        self,
        client: OpenAI,
        model: str,
        tools: ToolRegistry,
        max_tokens: int = 4000,
    ) -> None:
        self.client = client
        self.model = model
        self.tools = tools
        self.max_tokens = max_tokens
        self.messages: list = []

    def run(self, prompt: str) -> str:
        """Run the agent with a user prompt and return the final response."""
        self.messages = [{"role": "user", "content": prompt}]

        while True:
            response = self._chat()

            if not response.choices:
                raise RuntimeError("No choices in response")

            message = response.choices[0].message
            self.messages.append(message)

            # Check if done (no tool calls)
            if not message.tool_calls:
                return message.content or ""

            # Handle tool calls
            self._handle_tool_calls(message.tool_calls)

    def _chat(self):
        """Make a chat completion request."""
        return self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,  # type: ignore[arg-type]
            tools=self.tools.to_openai_schema(),  # type: ignore[arg-type]
            max_tokens=self.max_tokens,
        )

    def _handle_tool_calls(self, tool_calls) -> None:
        """Execute tool calls and add results to messages."""
        for tool_call in tool_calls:
            if tool_call.type != "function":
                print(f"Unknown tool call type: {tool_call.type}", file=sys.stderr)
                continue

            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            try:
                result = self.tools.execute(name, **args)
            except (KeyError, FileNotFoundError, ValueError, OSError) as e:
                result = f"Error: {e}"

            print(f"Tool call: {name}({tool_call.function.arguments}) -> {result}", file=sys.stderr)

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
