# -*- coding: utf-8 -*-

"""Test case for lexer."""

from llb3d import lexer

def eq_token(token, type, value):
    if isinstance(value, float) and isinstance(token.value, float):
        return token.type == type and abs(token.value - value) <= 0.001
    else:
        return token.type == type and token.value == value

def test_keywords():
    keywords = [
        "After", "And", "Before", "Case", "Const", "Data", "Default",
        "Delete", "Dim", "Each", "Else", "ElseIf", "End", "EndIf",
        "Exit", "False", "Field", "First", "Float", "For", "Forever",
        "Function", "Global", "Gosub", "Goto", "If", "Insert", "Int",
        "Last", "Local", "Mod", "New", "Next", "Not", "Null", "Or", "Pi",
        "Read", "Repeat", "Restore", "Return", "Sar", "Select", "Shl",
        "Shr", "Step", "Str", "Then", "To", "True", "Type", "Until",
        "Wend", "While", "Xor", "Include"
    ]

    code = " ".join(keywords)

    error_list, lexems = lexer.get_lexems(code)

    assert error_list == []
    assert len(lexems) == len(keywords)

    for i in range(len(keywords)):
        assert lexems[i].type == keywords[i].upper()
        assert lexems[i].value == keywords[i].upper()

def test_id():
    error_list, lexems = lexer.get_lexems('hello')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'ID', 'HELLO')

    error_list, lexems = lexer.get_lexems('player1')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'ID', 'PLAYER1')

    error_list, lexems = lexer.get_lexems('time_to_live')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'ID', 'TIME_TO_LIVE')

    error_list, lexems = lexer.get_lexems('t__')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'ID', 'T__')

    error_list, lexems = lexer.get_lexems('0x115')
    assert error_list == []
    assert len(lexems) == 2
    assert eq_token(lexems[0], 'INTVAL', 0)
    assert eq_token(lexems[1], 'ID', 'X115')

def test_symbols():
    code = '%#$(),.\n\\+-*/~^<>='
    error_list, lexems = lexer.get_lexems(code)
    assert error_list == []
    assert len(lexems) == len(code)
    for i in range(len(lexems)):
        assert eq_token(lexems[i], code[i], code[i])

def test_values():
    error_list, lexems = lexer.get_lexems('123456')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'INTVAL', 123456)

    error_list, lexems = lexer.get_lexems('123.456')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'FLOATVAL', 123.456)

    error_list, lexems = lexer.get_lexems('.6')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'FLOATVAL', .6)

    error_list, lexems = lexer.get_lexems('2.')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'FLOATVAL', 2)

    error_list, lexems = lexer.get_lexems('"Hello"')
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'STRVAL', 'Hello')

    error_list, lexems = lexer.get_lexems('"Hello" + "World!"')
    assert error_list == []
    assert len(lexems) == 3
    assert eq_token(lexems[0], 'STRVAL', 'Hello')
    assert eq_token(lexems[1], '+', '+')
    assert eq_token(lexems[2], 'STRVAL', 'World!')

def test_comments():
    code = 'for ; ever dream'
    error_list, lexems = lexer.get_lexems(code)
    assert error_list == []
    assert len(lexems) == 1
    assert eq_token(lexems[0], 'FOR', 'FOR')

def test_errors():
    error_list, lexems = lexer.get_lexems('What?')
    assert error_list == ["Illegal character '?' at 1:5"]

    error_list, lexems = lexer.get_lexems('\nWhat?')
    assert error_list == ["Illegal character '?' at 2:5"]

def test_spaces():
    code = """For i% = 1 to 10 ; Magic for
        Print i%
    End"""

    decode = [
        ('FOR', 'FOR'),
        ('ID', 'I'),
        ('%', '%'),
        ('=', '='),
        ('INTVAL', 1),
        ('TO', 'TO'),
        ('INTVAL', 10),
        ('\n', '\n'),
        ('ID', 'PRINT'),
        ('ID', 'I'),
        ('%', '%'),
        ('\n', '\n'),
        ('END', 'END')
    ]

    error_list, lexems = lexer.get_lexems(code)

    assert error_list == []
    assert len(lexems) == len(decode)

    for i in range(len(lexems)):
        assert eq_token(lexems[i], decode[i][0], decode[i][1])
