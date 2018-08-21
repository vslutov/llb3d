# -*- coding: utf-8 -*-

"""Test case for ast."""

from pytest import raises

from llb3d import ast

def test_expression():
    """Test expression class."""
    expr1 = ast.Expression("Hello, {name}!", name='Alice')
    assert expr1['name'] == 'Alice'
    assert str(expr1) == "Hello, Alice!"

    expr2 = ast.Expression("Hello, {name}!", {'name': 'Alice'})
    assert expr2['name'] == 'Alice'
    assert str(expr2) == "Hello, Alice!"

def test_line():
    """Test basic expression."""
    intval = ast.IntVal(123)
    assert intval['value'] == 123
    assert str(intval) == '123'

    var = ast.Variable('HELLO')
    assert var['name'] == 'HELLO'
    assert str(var) == 'HELLO'

    unary_op = ast.UnaryOp('-', var)
    assert unary_op['op'] == '-'
    assert unary_op['expr'] == var
    assert str(unary_op) == '- HELLO'

    binary_op = ast.BinaryOp('*', intval, unary_op)
    assert binary_op['op'] == '*'
    assert binary_op['left'] == intval
    assert binary_op['right'] == unary_op
    assert str(binary_op) == '(123 * - HELLO)'

    assign = ast.Assign(ast.Variable('LEFT'), binary_op)
    assert assign['var'] == ast.Variable('LEFT')
    assert assign['expr'] == binary_op
    assert str(assign) == 'LEFT = (123 * - HELLO)'

def test_sequence():
    """Test operator and expression sequence."""
    var1 = ast.Variable('VAR1')
    var2 = ast.Variable('VAR2')
    var3 = ast.Variable('VAR3')
    var4 = ast.Variable('VAR4')

    seq1 = ast.Sequence()
    seq1 = seq1.append(var1)
    seq1 = seq1.append(var2)

    assert seq1.dict['tuple'] == (var1, var2)
    assert seq1[0] == var1
    assert seq1[1] == var2

    assert isinstance(seq1[:], ast.Sequence)
    assert seq1[:] == seq1

    assert len(seq1) == len(seq1['tuple'])

    with raises(NotImplementedError):
        str(seq1)

    seq2 = seq1.append(var4)
    assert isinstance(seq2, ast.Sequence)
    assert seq2.list == [var1, var2, var4]

    seq1.append(var3)
    assert seq1.list == [var1, var2, var3]

    op_seq = ast.OperatorSequence()
    op_seq.list = seq1.list.copy()
    assert isinstance(op_seq, ast.Sequence)
    assert str(op_seq) == 'VAR1\nVAR2\nVAR3'

    ident = ast.Ident(op_seq)
    assert isinstance(ident, ast.Sequence)
    assert isinstance(ident, ast.OperatorSequence)
    assert str(ident) == '  VAR1\n  VAR2\n  VAR3'

    expr_seq = ast.ExpressionSequence()
    expr_seq.list = seq2.list.copy()
    assert isinstance(expr_seq, ast.Sequence)
    assert str(expr_seq) == 'VAR1, VAR2, VAR4'

def test_call():
    """Test function and procedure calls."""

    args = ast.ExpressionSequence()
    args.append(ast.BinaryOp('+', ast.Variable('6'), ast.Variable('5')))
    args.append(ast.BinaryOp('*', ast.Variable('7'), ast.Variable('8')))

    func_call = ast.FuncCall('HELLO', args)
    assert func_call.name == 'HELLO'
    assert func_call.args == args
    assert str(func_call) == 'HELLO((6 + 5), (7 * 8))'

    proc_call = ast.ProcCall('HELLO', args)
    assert proc_call.name == 'HELLO'
    assert proc_call.args == args
    assert str(proc_call) == 'HELLO (6 + 5), (7 * 8)'

def test_flow():
    """Test flow operators."""
    branch_1 = ast.OperatorSequence()
    branch_1.append(ast.Assign(ast.Variable('A'), ast.IntVal(5)))
    branch_1.append(ast.Assign(ast.Variable('B'), ast.IntVal(10)))

    branch_2 = ast.OperatorSequence()
    branch_2.append(ast.Assign(ast.Variable('B'), ast.IntVal(3)))
    branch_2.append(ast.Assign(ast.Variable('C'), ast.IntVal(1)))

    expr = ast.BinaryOp('+', ast.Variable('A'), ast.Variable('B'))
    expr = ast.BinaryOp('=', expr, ast.IntVal('5'))

    simple_if = ast.If(expr, branch_1, ast.OperatorSequence())
    assert simple_if.expr == expr
    assert simple_if.true_branch == branch_1
    assert str(simple_if) == 'IF ((A + B) = 5)\n  A = 5\n  B = 10\nENDIF'

    double_if = ast.If(expr, branch_1, branch_2)
    assert double_if.expr == expr
    assert double_if.true_branch == branch_1
    assert double_if.false_branch == branch_2
    assert str(double_if) == ('IF ((A + B) = 5)\n  A = 5\n  B = 10\nELSE\n' +
                              '  B = 3\n  C = 1\nENDIF')

    expr_list = ast.ExpressionSequence()
    expr_list.append(ast.Variable('A'))
    expr_list.append(ast.Variable('B'))
    expr_list.append(ast.Variable('C'))
    assert str(expr_list) == 'A, B, C'

    func = ast.FuncDef('HELLO', expr_list, branch_1)
    assert func.name == 'HELLO'
    assert func.args == expr_list
    assert func.body == branch_1
    assert str(func) == 'FUNCTION HELLO(A, B, C)\n  A = 5\n  B = 10\nEND FUNCTION'
