# -*- coding: utf-8 -*-

"""Test case for ast."""

from .. import ast

def test_identifier():
    """Test identifier class."""
    alice = ast.Identifier("Alice")
    assert alice['name'] == "Alice"
