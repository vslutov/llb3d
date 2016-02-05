# -*- coding: utf-8 -*-

"""Parser for Blitz3D language."""

from llb3d import ast, lexer
from lexer import tokens

from ply import yacc

class parser_globals:
    error_list = None

def init():
    parser_globals.error_list = []

start = 'program'

def p_empty(p):
    "empty : "
    pass

def p_atom_int(p):
    r"""atom : INTVAL"""
    p[0] = ast.IntVal(p[1])

def p_atom_var(p):
    r"""atom : ID"""
    p[0] = ast.Variable(p[1])

def p_binary(p):
    r"""rvalue : rvalue '+' term
               | rvalue '-' term
        term : term '*' factor
             | term '/' factor"""
    p[0] = ast.BinaryOp(p[2], p[1], p[3])

def p_rvalue_term(p):
    r"""rvalue : term
        term : factor
        factor : atom"""
    p[0] = p[1]

def p_factor_expr(p):
    r"""factor : '(' rvalue ')'"""
    p[0] = p[2]

def p_line_print(p):
    r"""line : rvalue"""
    p[0] = ast.UnaryOp(p[1], p[2])

def p_line_assign(p):
    r"""line : ID '=' rvalue"""
    p[0] = ast.Assign(p[1], p[3])

def p_program_line(p):
    r"""program : line"""
    p[0] = ast.Sequence([p[1]])

def p_program_rec(p):
    r"""program : program '\n' line"""
    p[0] = p[1].copy()
    p[0].append(p[3])

# Error rule for syntax errors
def p_error(p):
    if not p:
        parser_globals.error_list.append("Unexpected EOF")
        return

    parser_globals.error_list.append("Unexpected '{token}' at {position}"
                        .format(token=p.type, position=lexer.position(p)))

# Build the parser
parser = yacc.yacc()

def get_ast(code):
    """Get AST from the source code"""
    error_list, lexems = lexer.get_lexems(code)

    if error_list != []:
        return error_list, None

    lexer.init(code)
    init()
    syntax_tree = parser.parse(code.upper())

    return parser_globals.error_list, syntax_tree

error_list, syntax_tree = get_ast("""b = 256
        a = 12 - 6 - 3 * b""")

print(syntax_tree)
