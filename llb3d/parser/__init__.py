# -*- coding: utf-8 -*-

"""llb3d - Blitz3d parser."""

# -*- coding: utf-8 -*-

"""Parser for Blitz3D language."""

from llb3d import ast, lexer

from ply import yacc

from ..lexer import tokens

class ParserGlobals:
    """Global variables for parser."""

    def __init__(self):
        self.error_list = []

start = 'body'

def p_empty(p):
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
    if not p:
        p.parser.globals.error_list.append("Unexpected EOF")
        return

    p.parser.globals.error_list.append("Unexpected '{token}' at {position}"
                                       .format(token=p.type, position=lexer.position(p)))

def get_ast(code):
    """Get AST from the source code"""
    parser = yacc.yacc()
    parser.globals = ParserGlobals()
    syntax_tree = parser.parse(lexer=lexer.get_lexer(code))

    if parser.globals.error_list != []:
        raise SyntaxError("\n".join(parser.globals.error_list))

    return syntax_tree
