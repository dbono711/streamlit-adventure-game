# -*- mode: python; python-indent: 4 -*-
"""Docstring Missing."""
import os

import dotenv
import openai

dotenv.load_dotenv("secrets.env")

_AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
]


class OpenAi():
    """Docstring missing."""

    def __init__(self) -> None:
        """Docstring missing."""
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    def generate_response(self, content):
        """Docstring missing."""
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content},
            ],
            max_tokens = 1024,
        )

        return completion.choices[0].message.content
