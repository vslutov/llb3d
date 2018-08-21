# -*- coding: utf-8 -*-

"""Test case for ast."""

from .. import ast

def test_expression():
    """Test expression class."""
    expr1 = ast.Expression("Hello, {name}!", name='Alice')
    assert expr1['name'] == 'Alice'
    assert str(expr1) == "Hello, Alice!"
