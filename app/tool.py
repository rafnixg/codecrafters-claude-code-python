"""Base tool classes and registry."""

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """Base class for all tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name used for function calls."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for the LLM."""

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """JSON schema for tool parameters."""

    @abstractmethod
    def execute(self, **kwargs: Any) -> str:
        """Execute the tool with given arguments."""

    def to_openai_schema(self) -> dict[str, Any]:
        """Convert to OpenAI tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolRegistry:
    """Registry to manage and execute tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """Get a tool by name."""
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")
        return self._tools[name]

    def execute(self, name: str, **kwargs: Any) -> str:
        """Execute a tool by name with given arguments."""
        return self.get(name).execute(**kwargs)

    def to_openai_schema(self) -> list[dict[str, Any]]:
        """Convert all registered tools to OpenAI format."""
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def __len__(self) -> int:
        return len(self._tools)

    def __iter__(self):
        return iter(self._tools.values())
