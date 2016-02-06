# -*- coding: utf-8 -*-

"""Parser for Blitz3D language."""

from llb3d import ast, lexer
from lexer import tokens

from ply import yacc

class parser_globals:
    error_list = None

def init():
    parser_globals.error_list = []

start = 'body'

def p_empty(p):
    "empty : "
    pass

def p_atom_int(p):
    r"""atom : INTVAL"""
    p[0] = ast.IntVal(p[1])

def p_atom_var(p):
    r"""atom : ID"""
    p[0] = ast.Variable(p[1])

def p_atom_special(p):
    r"""atom : TRUE
             | FALSE
             | NULL
    """
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
    """
    p[0] = p[1]

def p_operator_assign(p):
    r"""operator : ID '=' rvalue"""
    p[0] = ast.Assign(p[1], p[3])

def p_funccall(p):
    r"""funccall : ID '(' rvaluelist ')'
        funccall : ID '(' empty ')'
    """
    p[0] = ast.CallFunc(p[1], p[3])

def p_operator_descent(p):
    r"""operator : empty
                 | funccall
    """
    p[0] = p[1]

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

def p_optelse_body(p):
    r"""optelse : ELSE '\n' body"""
    p[0] = p[3]

def p_optelse_empty(p):
    r"""optelse : empty"""
    p[0] = ast.OperatorSequence()

def p_operator_if_then(p):
    r"""operator : IF rvalue THEN '\n' body optelse endif"""
    p[0] = ast.If(p[2], p[5], p[6])

def p_operator_if_nonthen(p):
    r"""operator : IF rvalue '\n' body optelse endif"""
    p[0] = ast.If(p[2], p[4], p[5])

def p_optinlineelse_empty(p):
    r"""optinlineelse : empty"""
    p[0] = ast.OperatorSequence()

def p_optinlineelse_operator(p):
    r"""optinlineelse : ELSE operator"""
    p[0] = ast.OperatorSequence(p[2])

def p_operator_if_inline(p):
    r"""operator : IF rvalue THEN operator optinlineelse"""
    p[0] = ast.If(p[2], ast.OperatorSequence(p[4]), p[5])

# Function define
def p_operator_deffunc(p):
    r"""operator : FUNCTION ID '(' varlist ')' '\n' body '\n' END FUNCTION"""
    p[0] = ast.DefFunc(p[2], p[4], p[7])

# Body
def p_start(p):
    r"""body : operator"""
    p[0] = ast.OperatorSequence(p[1])

def p_var_start(p):
    r"""rvaluelist : rvalue
        varlist : ID
    """
    p[0] = ast.ExpressionSequence(p[1])

def p_append(p):
    r"""body : body '\n' operator
        rvaluelist : rvaluelist ',' rvalue
        varlist : varlist ',' ID
    """
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

error_list, syntax_tree = get_ast("""
Function Fib(n)
    If n = 0 or n = 1
        a = 10 + 15
        Return 1
    Else
        Return Fib(n - 2) + Fib(n - 1)
    EndIf
End Function

If True then b = 6
If False then c = 5 else d = 7
If b = 5 = 6
    Print 2 ; "b = 5 = 6"
End If

If 1 Then
    Print 1
EndIf

Print Fib(5)""")

if error_list == []:
    print(str(syntax_tree).lower())
else:
    for error in error_list:
        print(error)
