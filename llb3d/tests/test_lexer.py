# -*- coding: utf-8 -*-

"""Test case for lexer."""

from ply import lex
from pytest import raises

from .. import lexer

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

    lexems = tuple(lexer.get_lexer(code))

    assert tuple(EqToken(a, a) for a in lexer.keywords) == lexems

def test_keywords_case():
    """Check keyword case insensitive."""
    assert tuple(lexer.get_lexer('For')) == (EqToken('FOR', 'For'), )

def test_id():
    """Test all id from documentation."""
    lexems = tuple(lexer.get_lexer('hello'))
    assert (EqToken('ID', 'hello'), ) == lexems

    lexems = tuple(lexer.get_lexer('Player1'))
    assert (EqToken('ID', 'Player1'), ) == lexems

    lexems = tuple(lexer.get_lexer('time_to_live'))
    assert (EqToken('ID', 'time_to_live'), ) == lexems

    lexems = tuple(lexer.get_lexer('t__'))
    assert (EqToken('ID', 't__'), ) == lexems

def test_literal_symbol():
    """Check literal symbols."""
    lexems = tuple(lexer.get_lexer(lexer.literals))
    assert tuple(EqToken(a, a) for a in lexer.literals) == lexems

def test_literals():
    """Check literals."""
    lexems = tuple(lexer.get_lexer('123456'))
    assert (EqToken('INTLIT', 123456), ) == lexems

    lexems = tuple(lexer.get_lexer('123.456'))
    assert (EqToken('FLOATLIT', 123.456), ) == lexems

    lexems = tuple(lexer.get_lexer('.6'))
    assert (EqToken('FLOATLIT', .6), ) == lexems

    lexems = tuple(lexer.get_lexer('2.'))
    assert (EqToken('FLOATLIT', 2.0), ) == lexems

    lexems = tuple(lexer.get_lexer('"Hello"'))
    assert (EqToken('STRLIT', 'Hello'), ) == lexems

    lexems = tuple(lexer.get_lexer('"Hello" + "World!"'))
    assert (EqToken('STRLIT', 'Hello'),
            EqToken('+', '+'),
            EqToken('STRLIT', 'World!')) == lexems

def test_comments():
    """Test comments remove."""
    code = 'for ; ever dream'
    lexems = tuple(lexer.get_lexer(code))
    assert (EqToken('FOR', 'for'), ) == lexems

def test_errors():
    """Test error messages."""
    with raises(SyntaxError) as exc:
        tuple(lexer.get_lexer('What?'))
    assert exc.value.msg == "Illegal character '?' at 1:5"

    with raises(SyntaxError) as exc:
        tuple(lexer.get_lexer('\nWhat?'))
    assert exc.value.msg == "Illegal character '?' at 2:5"

def test_small_program():
    """Check small program."""

    code = """For i% = 1 To 10 ; Magic for
        Print i%
    Next"""

    decode = (
        EqToken('FOR', 'For'),
        EqToken('ID', 'i'),
        EqToken('%', '%'),
        EqToken('=', '='),
        EqToken('INTLIT', 1),
        EqToken('TO', 'To'),
        EqToken('INTLIT', 10),
        EqToken('\n', '\n'),
        EqToken('ID', 'Print'),
        EqToken('ID', 'i'),
        EqToken('%', '%'),
        EqToken('\n', '\n'),
        EqToken('NEXT', 'Next')
    )

    lexems = tuple(lexer.get_lexer(code))

    assert decode == lexems
