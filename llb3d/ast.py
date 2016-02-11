# -*- coding: utf-8 -*-

"""Ast for llb3d."""

from functools import wraps

IDENT = 2

def isfunction(obj):
    """Test, can we call an obj."""
    try:
        getattr(obj, '__call__')
        return True
    except AttributeError:
        return False

class Expression:

    """Basic expression."""

    def __str__(self):
        raise NotImplementedError()

class IntVal(Expression):

    """Integer."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Variable(Expression):

    """Variable."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class BinaryOp(Expression):

    """Binary operator."""

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return '({left} {op} {right})'.format(left=self.left, right=self.right,
                                              op=self.op)

class UnaryOp(Expression):

    """Unary operator."""

    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    def __str__(self):
        return '{op} {arg}'.format(op=self.op, arg=self.arg)

class Assign(Expression):

    """Assign operator."""

    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __str__(self):
        return '{var} = {expr}'.format(var=self.var, expr=self.expr)

class Sequence(Expression):

    """Sequence of operators or expressions."""

    def __init__(self, first=None):
        if first is not None:
            self.list = [first]
        else:
            self.list = []

    def __getattr__(self, name):
        res = getattr(self.list, name)

        if isfunction(res):

            @wraps(res)
            def wrapper(*args, **kwds):
                """I result is list, we should return elem with right type."""
                result = res(*args, **kwds)
                if isinstance(result, list):
                    new_result = type(self)()
                    new_result.list = result

                    return new_result
                else:
                    return result

            return wrapper

        else:
            return res

    def __len__(self):
        return self.__getattr__('__len__')()

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return self.list == other.list
        elif isinstance(other, list):
            return self.list == other
        else:
            return False

class OperatorSequence(Sequence):
    """Operator sequence."""
    def __str__(self):
        return '\n'.join(str(elem) for elem in self.list)

class ExpressionSequence(Sequence):
    """Expression sequence."""
    def __str__(self):
        return ', '.join(str(elem) for elem in self.list)

class Ident(OperatorSequence):

    """Identation operator sequence."""

    def __init__(self, sequence):
        super().__init__()
        self.list = sequence.list.copy()

    def __str__(self):
        body = super().__str__().split('\n')
        return '\n'.join(' ' * IDENT + line for line in body)

class If(Expression):

    """If expression."""

    def __init__(self, expr, true_branch, false_branch):
        self.expr = expr
        self.true_branch = Ident(true_branch)
        self.false_branch = Ident(false_branch)

    def __str__(self):
        if len(self.false_branch) == 0:
            return ('IF {expr}\n{true_branch}\nENDIF'
                    .format(expr=self.expr, true_branch=self.true_branch))
        else:
            return ('IF {expr}\n{true_branch}\nELSE\n{false_branch}\nENDIF'
                    .format(expr=self.expr, true_branch=self.true_branch,
                            false_branch=self.false_branch))

class FuncDef(Expression):

    """Function definition."""

    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = Ident(body)

    def __str__(self):
        return ('FUNCTION {name}({args})\n{body}\nEND FUNCTION'
                .format(name=self.name, args=self.args, body=self.body))

class FuncCall(Expression):

    """Function call."""

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return '{func}({args})'.format(func=self.name, args=self.args)

class ProcCall(FuncCall):

    """Procedure call."""

    def __str__(self):
        return '{func} {args}'.format(func=self.name, args=self.args)

