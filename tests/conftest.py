# -*- mode: python; python-indent: 4 -*-
"""Docstring missing."""
import pytest

from mage import Mage


@pytest.fixture(scope="module")
def mage():
    return Mage()