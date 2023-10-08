# -*- mode: python; python-indent: 4 -*-
"""Docstring missing."""
import re

import streamlit as st

from mage import Mage
from openaichat import OpenAi

_CHARACTERS = ["", "Warrior", "Hunter", "Mage"]


class Application(OpenAi):
    """Docstring missing."""

    def __init__(self):
        """Docstring missing."""
        OpenAi.__init__(self)

        if 'start' not in st.session_state:
            st.session_state.start = False
        
        if "messages" not in st.session_state.keys():
            self.initialize_chat()
    
    def initialize_chat(self) -> None:
        st.session_state.messages = [
            {"role": "assistant", "content": "Select a character on the left to begin"}
        ]
        st.session_state.start = False
    
    def get_selection(self, number, response):
        """Docstring missing."""
        pattern = rf"{number}\.\s(.*?):"
        match = re.search(pattern, response)
        
        return match.group(1) if re.search(pattern, response) else None
    
    def click_button(self, name):
        st.session_state[name] = True
    
    def main(self):
        """Docstring missing."""
        st.set_page_config(layout="wide", page_title="Streamlit Adventure Game")
        st.header("Streamlit Adventure Game")
        character_selection = st.sidebar.selectbox("Select a character", _CHARACTERS, key="character")

        if character_selection == "Mage":
            character = Mage()

        if character_selection:
            st.sidebar.write(f"**Character:** {character_selection}")
            st.sidebar.write(f"**Weapon:** {character.weapon}")
            st.sidebar.button("Start!", on_click=self.click_button, args=('start',))

        # if "messages" not in st.session_state.keys():
        #     st.session_state.messages = [
        #         {
        #             "role": "assistant",
        #             "content": "Select a character on the left to begin"
        #         }
        #     ]
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # if st.session_state.start:
        #     with st.chat_message("assistant"):
        #         with st.spinner("Generating Adventure..."):
        #             response = self.generate_response(
        #                 f"""
        #                 In no more than 250 words, create an introduction to a story in 
        #                 Medieval times about a {character_selection} with a magical 
        #                 {character.weapon} on a quest. Provide 4 choices as numbered 
        #                 selections, each with a title, for the {character_selection} 
        #                 to choose from.
        #                 """
        #             )
        #             st.write(response)

        #     message = {"role": "assistant", "content": response}
        #     st.session_state.messages.append(message)

        #     with st.chat_message("assistant"):
        #         st.write("Choose your path...")
            
        #     choices = []
        #     for item in [1, 2, 3, 4]:
        #         choices.append(self.get_selection(item, response))
            
        #     st.write(choices)
        
        st.sidebar.button("Restart Game", on_click=self.initialize_chat, key="clear")


        # if prompt := st.chat_input(disabled=not(character_selection)):
        #     st.session_state.messages.append({"role": "user", "content": prompt})
        #     with st.chat_message("user"):
        #         st.write(prompt)
        
        # if st.session_state.messages[-1]["role"] != "assistant":
        #     with st.chat_message("assistant"):
        #         with st.spinner("Thinking..."):
        #             response = self.generate_response(prompt) 
        #             st.write(response) 
        #     message = {"role": "assistant", "content": response}
        #     st.session_state.messages.append(message)

if __name__ == '__main__':
    Application().main()
