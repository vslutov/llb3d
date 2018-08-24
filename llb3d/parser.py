# -*- coding: utf-8 -*-

"""Parser for Blitz3D language."""

#pylint: disable=invalid-name

from ply import yacc

from . import ast, lexer

from .lexer import tokens #pylint: disable=unused-import

class ParserGlobals:
    """Global variables for parser."""

    def __init__(self):
        """Global variables for parser."""
        self.error_list = []

start = 'body'

def p_empty(_p):
    "empty : "
    pass

def p_atom(p):
    r"""atom : INTLIT"""
    p[0] = ast.IntLiteral(int(p[1]))

# Body
def p_start(p):
    r"""body : atom"""
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    """Error handler."""
    if not p:
        parser.globals.error_list.append("Unexpected EOF")
        return

    parser.globals.error_list.append("Unexpected {type} '{value}' at {position}"
                                     .format(type=p.type, value=p.value,
                                             position=lexer.position(p)))

parser = yacc.yacc()

def get_ast(code):
    """Get AST from the source code."""
    parser.globals = ParserGlobals()
    syntax_tree = parser.parse(lexer=lexer.get_lexer(code))

    if parser.globals.error_list != []:
        raise SyntaxError("\n".join(parser.globals.error_list))

    return syntax_tree
