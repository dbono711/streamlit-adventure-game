# -*- mode: python; python-indent: 4 -*-
"""Docstring Missing."""
import re

from loggerfactory import LoggerFactory


class Toolbox():
    """Docstring missing."""

    def __init__(self):
        """Docstring missing."""
        self.logger = LoggerFactory.get_logger("app.py", log_level="WARNING")
    
    def get_selection(self, number, response):
        """Docstring missing."""
        pattern = rf"{number}\.\s(.*?):"
        match = re.search(pattern, response)
        
        return match.group(1) if re.search(pattern, response) else None
