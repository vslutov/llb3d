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

start = 'program'

# Empty

def p_empty(_p):
    "empty : "

# Statements

def p_statement_descent(p):
    r"""global_statement : statement
        local_statement : statement
    """
    p[0] = p[1]

def p_statements_start(p):
    r"""global_statements : global_statement
        local_statements : local_statement
    """
    p[0] = ast.Body((p[1], ))

def p_statement_rest(p):
    r"""global_statements : global_statements '\n' global_statement
        local_statements : local_statements '\n' local_statement
    """
    p[0] = ast.Body(p[1]['statements'] + (p[3], ))


# Identifier

def p_id(p):
    r"""id : ID"""
    p[0] = ast.Identifier(p[1])

# Literals

def p_atom_int(p):
    r"""atom : INTLIT"""
    p[0] = ast.IntLiteral(int(p[1]))

def p_atom_float(p):
    r"""atom : FLOATLIT"""
    p[0] = ast.FloatLiteral(float(p[1]))

def p_atom_string(p):
    r"""atom : STRLIT"""
    p[0] = ast.StrLiteral(p[1])

def p_atom_id(p):
    r"""atom : id"""
    p[0] = p[1]

# Expression

def p_expression_descent(p):
    r"""expression : atom
        statement : expression
    """
    p[0] = p[1]

def p_exprlist_start(p):
    r"""exprlist : expression"""
    p[0] = (p[1], )

def p_exprlist_rest(p):
    r"""exprlist : exprlist ',' expression"""
    p[0] = p[1] + (p[3], )

# Procedure call

def p_statement_proccall(p):
    r"""statement : proccall"""
    p[0] = p[1]

def p_proccall(p):
    r"""proccall : id exprlist
                 | id empty
    """
    if p[2] is None:
        p[0] = ast.ProcedureCall(p[1], tuple())
    else:
        p[0] = ast.ProcedureCall(p[1], p[2])

# Program

def p_start(p):
    r"""program : global_statements"""
    p[0] = ast.Program(p[1]['statements'])

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
