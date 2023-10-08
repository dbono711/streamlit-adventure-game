# -*- mode: python; python-indent: 4 -*-
"""Docstring Missing."""

from loggerfactory import LoggerFactory


class Toolbox():
    """Docstring missing."""

    def __init__(self):
        """Docstring missing."""
        self.logger = LoggerFactory.get_logger("app.py", log_level="WARNING")
