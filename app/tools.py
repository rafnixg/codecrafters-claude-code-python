"""Tools for the application."""
import os


def read_file(file_path: str) -> str:
    """Read and return the contents of a file"""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
