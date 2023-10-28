# -*- mode: python; python-indent: 4 -*-
"""Docstring Missing."""
import random

import streamlit as st

from loggerfactory import LoggerFactory


class Toolbox():
    """Docstring missing."""

    def __init__(self):
        """Docstring missing."""
        self.logger = LoggerFactory.get_logger("app.py", log_level="WARNING")

    def cast_selection(self, key):
        key["active"] = True
        key["disabled"] = True
        
        if st.session_state["start"]["disabled"]:
            self.generate_numbers()
    
    def generate_numbers(self):
        """Docstring missing."""
        for stat in ("health", "magic", "coins"):
            current = st.session_state["character"][stat]["value"]
            new = random.randrange(0, 100, 1)

            st.session_state["character"][stat]["value"] = new
            st.session_state["character"][stat]["delta"] = (new - current) + 10