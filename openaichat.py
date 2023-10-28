# -*- mode: python; python-indent: 4 -*-
"""Docstring Missing."""
import os

import dotenv
import openai
import streamlit as st

dotenv.load_dotenv("secrets.env")


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

        response = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        return response
