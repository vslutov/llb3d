# -*- coding: utf-8 -*-

"""Tests for Blitz3D parser."""

from pytest import raises

from .. import parser, ast

def test_intlit():
    """Check integer literal parser."""
    assert parser.get_ast('10') == ast.IntLiteral(10)

def test_floatlit():
    """Check float literal parser."""
    assert parser.get_ast('10.5') == ast.FloatLiteral(10.5)

def test_strlit():
    """Check string literal parser."""
    assert parser.get_ast('"Hello"') == ast.StrLiteral("Hello")

def test_error():
    """Check error log."""
    with raises(SyntaxError) as exc:
        parser.get_ast('10 20')

    assert exc.value.msg == "Unexpected INTLIT '20' at 1:4"
