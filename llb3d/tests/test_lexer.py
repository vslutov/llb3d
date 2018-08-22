# -*- coding: utf-8 -*-

"""Test case for lexer."""

from ply import lex
from llb3d import lexer

class EqToken:
    """Utility class to check equal lexems."""

    def __init__(self, type_, value):
        """Initialize self.  See help(type(self)) for accurate signature."""
        self.type = type_
        self.value = value

    def __eq__(self, other):
        """Test equal."""
        print(self, other)
        assert isinstance(other, lex.LexToken)
        assert self.type == other.type

        if isinstance(self.value, float):
            assert isinstance(other.value, float)
            assert abs(other.value - self.value) <= 0.001
        else:
            assert self.value == other.value

        return True

    def __repr__(self):
        return "EqToken('{type}', '{value}')".format(type=self.type, value=self.value)

def test_keywords():
    """Test that keywords is tokens with type and value keywords."""
    code = " ".join(lexer.keywords)

    error_list, lexems = lexer.get_lexems(code)

    assert error_list == []
    assert [EqToken(a, a) for a in lexer.keywords] == lexems

def test_id():
    """Test all id from documentation."""
    error_list, lexems = lexer.get_lexems('hello')
    assert error_list == []
    assert [EqToken('ID', 'HELLO')] == lexems

    error_list, lexems = lexer.get_lexems('player1')
    assert error_list == []
    assert [EqToken('ID', 'PLAYER1')] == lexems

    error_list, lexems = lexer.get_lexems('time_to_live')
    assert error_list == []
    assert [EqToken('ID', 'TIME_TO_LIVE')] == lexems

    error_list, lexems = lexer.get_lexems('t__')
    assert error_list == []
    assert [EqToken('ID', 'T__')] == lexems

def test_literal_symbol():
    """Check literal symbols."""
    error_list, lexems = lexer.get_lexems(lexer.literals)
    assert error_list == []
    assert [EqToken(a, a) for a in lexer.literals] == lexems

def test_literals():
    """Check literals."""
    error_list, lexems = lexer.get_lexems('123456')
    assert error_list == []
    assert [EqToken('INTLIT', 123456)] == lexems

    error_list, lexems = lexer.get_lexems('123.456')
    assert error_list == []
    assert [EqToken('FLOATLIT', 123.456)] == lexems

    error_list, lexems = lexer.get_lexems('.6')
    assert error_list == []
    assert [EqToken('FLOATLIT', .6)] == lexems

    error_list, lexems = lexer.get_lexems('2.')
    assert error_list == []
    assert [EqToken('FLOATLIT', 2.0)] == lexems

    error_list, lexems = lexer.get_lexems('"Hello"')
    assert error_list == []
    assert [EqToken('STRLIT', 'Hello')] == lexems

    error_list, lexems = lexer.get_lexems('"Hello" + "World!"')
    assert error_list == []
    assert [EqToken('STRLIT', 'Hello'),
            EqToken('+', '+'),
            EqToken('STRLIT', 'World!')] == lexems

def test_comments():
    """Test comments remove."""
    code = 'for ; ever dream'
    error_list, lexems = lexer.get_lexems(code)
    assert error_list == []
    assert [EqToken('FOR', 'FOR')] == lexems

def test_errors():
    """Test error messages."""
    error_list, lexems = lexer.get_lexems('What?')
    assert error_list == ["Illegal character '?' at 1:5"]
    assert [EqToken('ID', 'WHAT')] == lexems

    error_list, lexems = lexer.get_lexems('\nWhat?')
    assert error_list == ["Illegal character '?' at 2:5"]
    assert [EqToken('\n', '\n'), EqToken('ID', 'WHAT')] == lexems

def test_small_program():
    """Check small program."""

    code = """For i% = 1 to 10 ; Magic for
        Print i%
    End"""

    decode = [
        EqToken('FOR', 'FOR'),
        EqToken('ID', 'I'),
        EqToken('%', '%'),
        EqToken('=', '='),
        EqToken('INTLIT', 1),
        EqToken('TO', 'TO'),
        EqToken('INTLIT', 10),
        EqToken('\n', '\n'),
        EqToken('ID', 'PRINT'),
        EqToken('ID', 'I'),
        EqToken('%', '%'),
        EqToken('\n', '\n'),
        EqToken('END', 'END')
    ]

    error_list, lexems = lexer.get_lexems(code)

    assert error_list == []
    assert decode == lexems
