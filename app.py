# -*- mode: python; python-indent: 4 -*-
"""Docstring missing."""
import streamlit as st

from hunter import Hunter
from knight import Knight
from mage import Mage
from openaichat import OpenAi
from toolbox import Toolbox

_CHARACTERS = ["", "Knight", "Hunter", "Mage"]
_PATH_CHOICES = ["North", "South", "East", "West"]


class Application(OpenAi, Toolbox):
    """Docstring missing."""

    def __init__(self):
        """Docstring missing."""
        OpenAi.__init__(self)
        Toolbox.__init__(self)
        
        if "messages" not in st.session_state.keys():
            self.initialize()
    
    def initialize(self) -> None:
        st.session_state.messages = []
        st.session_state.character = {
            "active": False,
            "disabled": False,
            "health": {
                "value": 110,
                "delta": 0
            },
            "magic": {
                "value": 50,
                "delta": 0
            },
            "coins": {
                "value": 200,
                "delta": 0
            }
        }
        st.session_state.character_selection = ""
        st.session_state.start = {"active": False, "disabled": False}
        st.session_state.intro = {"active": True, "disabled": False}
        st.session_state.first = {"active": False, "disabled": False}
        st.session_state.second = {"active": False, "disabled": False}
        st.session_state.third = {"active": False, "disabled": False}
        st.session_state.conclusion = {"active": False, "disabled": False}
    
    def continue_journey(self, path, character, image):
        """Docstring missing."""
        if selection := st.radio(
            "Choose your path...",
            _PATH_CHOICES,
            label_visibility="visible",
            horizontal=True,
            index=None,
            on_change=self.cast_selection,
            args=(st.session_state[path],),
            disabled=st.session_state[path]["disabled"],
            key=f"{path}_selection"
        ):

            with st.spinner(f"Contuining on to the {selection}..."):
                response = self.generate_response(
                    f"""
                    In no more than 150 words, continue the story with the
                    {character.character} selecting the {selection} path with the
                    {character.character}'s health now at 
                    {st.session_state["character"]["health"]["value"]} and magic at
                    {st.session_state["character"]["magic"]["value"]}. Provide 
                    four additional paths for the {character.character} to take as 
                    either "North", "South", "East, or "West".
                    """
                )

            col1, col2 = st.columns(2)
            with col1.chat_message("assistant"):
                st.markdown(response)
            
            col2.image(f"https://picsum.photos/id/{image}/300/300")
            
            st.session_state[path]["active"] = False
    
    def end_journey(self, path, character, image):
        """Docstring missing."""
        if selection := st.radio(
            "Choose your final path...",
            _PATH_CHOICES,
            label_visibility="visible",
            horizontal=True,
            index=None,
            on_change=self.cast_selection,
            args=(st.session_state[path],),
            disabled=st.session_state[path]["disabled"],
            key=f"{path}_selection"
        ):

            with st.spinner(f"Ending the journey in the {selection}..."):
                response = self.generate_response(
                    f"""
                    In no more than 150 words, end the story with the
                    {character.character} in the {selection} path with the
                    {character.character}'s health now at 
                    {st.session_state["character"]["health"]["value"]} and magic at
                    {st.session_state["character"]["magic"]["value"]}.
                    """
                )

            col1, col2 = st.columns(2)
            with col1.chat_message("assistant"):
                st.markdown(response)
            
            col2.image(f"https://picsum.photos/id/{image}/300/300")
            
            st.session_state[path]["active"] = False

    def main(self):
        """Docstring missing."""
        st.set_page_config(
            layout="wide",
            page_title="Streamlit Adventure Game",
            page_icon=":mountain:"
        )
        st.title("Streamlit Adventure Game")
        st.caption(":mountain: A Streamlit adventure game powered by OpenAI LLM")
        st.sidebar.caption("Select a character and press 'Start!'")
        st.sidebar.selectbox(
            "Select a character",
            _CHARACTERS,
            on_change=self.cast_selection,
            args=(st.session_state["character"],),
            disabled=st.session_state["character"]["disabled"],
            key="character_selection"
        )

        match st.session_state.character_selection:
            case "Mage":
                character = Mage()
            case "Hunter":
                character = Hunter()
            case "Knight":
                character = Knight()
        
        if st.session_state.character_selection:
            st.sidebar.button(
                "Start!",
                on_click=self.cast_selection,
                args=(st.session_state["start"],),
                disabled=st.session_state["start"]["disabled"],
                use_container_width=True
            )
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        if st.session_state["start"]["active"]:

            if st.session_state["intro"]["active"]:
                with st.spinner("Generating Adventure..."):
                    intro = self.generate_response(
                        f"""
                        In no more than 150 words, create an introduction to a story in 
                        Medieval times about a {character.character} with a legendary 
                        {character.weapon} on a quest. Provide four paths for the
                        {character.character} to take as either "North", "South", "East, 
                        or "West".
                        """
                    )

                col1, col2 = st.columns(2)
                with col1.chat_message("assistant"):
                    st.markdown(intro)
                
                col2.image("https://picsum.photos/id/10/300/300")
            
                st.session_state["intro"]["active"] = False
                st.session_state["first"]["active"] = True
        
            if st.session_state["first"]["active"] and not st.session_state["intro"]["active"]:
                self.continue_journey("first", character, 28)
                st.session_state["second"]["active"] = True
            
            if st.session_state["second"]["active"] and not st.session_state["first"]["active"]:
                self.continue_journey("second", character, 46)
                st.session_state["third"]["active"] = True
            
            if st.session_state["third"]["active"] and not st.session_state["second"]["active"]:
                self.continue_journey("third", character, 49)
                st.session_state["conclusion"]["active"] = True
            
            if st.session_state["conclusion"]["active"] and not st.session_state["third"]["active"]:
                self.end_journey("conclusion", character, 81)

        if st.session_state["character"]["active"]:
            st.sidebar.button(
                "Reset Game",
                on_click=self.initialize,
                use_container_width=True
            )
            st.sidebar.divider()
            st.sidebar.subheader(f"{character.character_icon} {character.character}")
            st.sidebar.metric(
                "Health",
                st.session_state["character"]["health"]["value"],
                delta=st.session_state["character"]["health"]["delta"]
            )
            st.sidebar.metric(
                "Magic",
                st.session_state["character"]["magic"]["value"],
                delta=st.session_state["character"]["magic"]["delta"]
            )
            st.sidebar.metric(
                "Coins",
                st.session_state["character"]["coins"]["value"],
                delta=st.session_state["character"]["coins"]["delta"]
            )


if __name__ == '__main__':
    Application().main()
