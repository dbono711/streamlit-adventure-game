# -*- mode: python; python-indent: 4 -*-
"""Docstring missing."""
import streamlit as st

from mage import Mage
from openaichat import OpenAi
from toolbox import Toolbox

_CHARACTERS = ["", "Warrior", "Hunter", "Mage"]


class Application(OpenAi, Toolbox):
    """Docstring missing."""

    def __init__(self):
        """Docstring missing."""
        OpenAi.__init__(self)
        Toolbox.__init__(self)
        
        if "messages" not in st.session_state.keys():
            self.initialize_chat()
    
    def initialize_chat(self) -> None:
        st.session_state.messages = []
        st.session_state.start = {"active": False, "disabled": False}
        st.session_state.character = {"active": False, "disabled": False}
        st.session_state.first_path = {"active": False, "disabled": False}
        st.session_state.second_path = {"active": False, "disabled": False}
        st.session_state.character_selection = None
    
    def click_button(self, name):
        st.session_state[name]["active"] = True
        st.session_state[name]["disabled"] = True
    
    def main(self):
        """Docstring missing."""
        st.set_page_config(layout="wide", page_title="Streamlit Adventure Game")
        st.header("Streamlit Adventure Game")
        st.markdown(
            "###### _Welcom to the my Streamlit Adventure Game! To begin, select a charcter on \
            the left and press 'Start!'_"
        )
        st.sidebar.selectbox(
            "Select a character",
            _CHARACTERS,
            on_change=self.click_button,
            args=('character',),
            disabled=st.session_state["character"]["disabled"],
            key="character_selection"
        )

        match st.session_state.character_selection:
            case "Mage":
                character = Mage()

        if st.session_state.character_selection:
            st.sidebar.write(f"**Character:** {st.session_state.character_selection}")
            st.sidebar.write(f"**Weapon:** {character.weapon}")
            st.sidebar.button(
                "Start!",
                on_click=self.click_button,
                args=('start',),
                disabled=st.session_state["start"]["disabled"],
                use_container_width=True
            )

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        if st.session_state["start"]["active"]:
            with st.spinner("Generating Adventure..."):
                intro = self.generate_response(
                    f"""
                    In no more than 200 words, create an introduction to a story in 
                    Medieval times about a {st.session_state.character_selection} with 
                    a magical {character.weapon} on a quest. Provide 4 choices as 
                    numbered selections, each with a title, for the 
                    {st.session_state.character_selection} to choose from.
                    """
                )

                st.session_state.messages.append(
                    {"role": "assistant", "content": intro}
                )

            with st.chat_message("assistant"):
                st.markdown(intro)
            
            st.session_state["start"]["active"] = False
            st.session_state["first_path"]["active"] = True
            st.session_state.first_path_choices = [
                self.get_selection(item, intro) for item in range(1,5)
            ]

        if st.session_state["first_path"]["active"]:
            if first_path_selection := st.radio(
                "Choose your path...",
                st.session_state.first_path_choices,
                label_visibility="visible",
                horizontal=True,
                index=None,
                on_change=self.click_button,
                args=('first_path',),
                disabled=st.session_state["first_path"]["disabled"],
                key="first_path_selection"
            ):

                with st.spinner(f"Contuining on to the {first_path_selection}..."):
                    path = self.generate_response(
                        f"""
                        In no more than 150 words, continue the story with the
                        {st.session_state.character_selection} selecting the 
                        {first_path_selection} path. Provide 4 additional choices as 
                        numbered selections, each with a title to choose from.
                        """
                    )

                with st.chat_message("assistant"):
                    st.markdown(path)
                
                st.session_state["second_path"]["active"] = True

        if st.session_state["character"]["active"]:
            st.sidebar.button(
                "Reset Game",
                on_click=self.initialize_chat,
                use_container_width=True
            )

if __name__ == '__main__':
    Application().main()
