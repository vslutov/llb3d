# -*- coding: utf-8 -*-

"""Test case for ast."""

from pytest import raises
from enforce.exceptions import RuntimeTypeError

from .. import ast

def test_frosen_dict():
    """Test frozen dict."""
    frozen_dict = ast.FrozenDict(a=10, b=20)
    assert len(frozen_dict) == 2
    assert ['a', 'b'] == sorted(frozen_dict)
    assert frozen_dict['a'] == 10
    assert frozen_dict['b'] == 20

    with raises(KeyError):
        print(frozen_dict['c'])

    assert frozen_dict != {'a': 10, 'b': 20}

    other_frozen_dict = ast.FrozenDict(a=10, b=20)

    assert hash(frozen_dict) == hash(other_frozen_dict)
    assert frozen_dict == other_frozen_dict

def test_abstract_literal():
    """Test abstract literal."""
    value = 10
    lit = ast.Literal(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == 'Literal(10)'

def test_integer_literal():
    """Test abstract literal."""
    value = 10

    lit = ast.IntLiteral(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == 'IntLiteral({value})'.format(value=value)

    with raises(RuntimeTypeError):
        ast.IntLiteral('string')

def test_float_literal():
    """Test float literal."""
    value = 10.0

    lit = ast.FloatLiteral(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == 'FloatLiteral({value})'.format(value=value)

    with raises(RuntimeTypeError):
        ast.FloatLiteral('string')

def test_string_literal():
    """Test string literal."""
    value = 'abacaba'

    lit = ast.StrLiteral(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == "StrLiteral('{value}')".format(value=value)

    with raises(RuntimeTypeError):
        ast.StrLiteral(10)
