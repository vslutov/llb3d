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

def p_atom_brackets(p):
    r"""atom : '(' rvalue ')'"""
    p[0] = p[2]

def p_unary(p):
    r"""unary : BEFORE unary
              | AFTER unary
              | INT unary
              | FLOAT unary
              | STR unary
              | '+' unary
              | '-' unary
              | '~' unary
        atom : NEW ID
             | FIRST ID
             | LAST ID
        operator : RETURN rvalue
    """
    p[0] = ast.UnaryOp(p[1], p[2])

def p_binary_append(p):
    r"""power : power '^' unary
        mult : mult '*' power
        mult : mult '/' power
        mult : mult MOD power
        shift : shift SHL mult
        shift : shift SHR mult
        shift : shift SAR mult
        arith : arith '+' shift
        arith : arith '-' shift
        comp : comp '>' arith
        comp : comp '<' arith
        comp : comp '=' arith
        bitwise : bitwise AND comp
        bitwise : bitwise OR comp
        bitwise : bitwise XOR comp
        negation : NOT bitwise
    """
    p[0] = ast.BinaryOp(p[2], p[1], p[3])

def p_binary_appendcomp(p):
    r"""comp : comp '<' '=' arith
             | comp '>' '=' arith
             | comp '<' '>' arith
    """
    p[0] = ast.BinaryOp(p[2] + p[3], p[1], p[4])

def p_descent(p):
    r"""atom : funccall
        unary : atom
        power : unary
        mult : power
        shift : mult
        arith : shift
        comp : arith
        bitwise : comp
        negation : bitwise
        rvalue : negation
        operator : funccall
        operator : if
        operator : empty
    """
    p[0] = p[1]

def p_operator_assign(p):
    r"""operator : ID '=' rvalue"""
    p[0] = ast.Assign(p[1], p[3])

def p_val_start(p):
    r"""rvaluelist : rvalue
        varlist : ID
    """
    p[0] = ast.ExpressionSequence(p[1])

def p_append(p):
    r"""program : program '\n' globop
        body : body '\n' operator
        rvaluelist : rvaluelist ',' rvalue
        varlist : varlist ',' ID
    """
    p[0] = p[1].copy()
    p[0].append(p[3])

def p_funccall(p):
    r"""funccall : ID '(' rvaluelist ')'
        funccall : ID '(' empty ')'
    """
    p[0] = ast.CallFunc(p[1], p[3])

def p_operator_proccall(p):
    r"""operator : ID rvaluelist
        operator : ID empty
    """
    p[0] = ast.CallProc(p[1], p[2])

# If construction
def p_endif(p):
    r"""endif : ENDIF
              | END IF
    """
    pass

def p_if_long(p):
    r"""if : IF rvalue THEN '\n' body endif"""
    p[0] = ast.If(p[2], p[5])

def p_if_short(p):
    r"""if : IF rvalue '\n' body '\n' endif
        if : IF rvalue THEN operator"""
    p[0] = ast.If(p[2], p[4])

# Function define
def p_deffunc(p):
    r"""deffunc : FUNCTION ID '(' varlist ')' '\n' body '\n' END FUNCTION"""
    p[0] = ast.DefFunc(p[2], p[4], p[7])

def p_globop(p):
    r"""globop : body
               | deffunc"""
    p[0] = p[1]

def p_start(p):
    r"""program : globop
        body : operator
    """
    p[0] = ast.OperatorSequence(p[1])

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

error_list, syntax_tree = get_ast("""
; Function Fib(n)
    If n = 0 or n = 1
        Return 1
    ;Else
        Return Fib(n - 2) + Fib(n - 1)
    EndIf
; End Function

Print Fib(5)""")

if error_list == []:
    print(syntax_tree)
else:
    for error in error_list:
        print(error)
