# -*- coding: utf-8 -*-

"""Ast for llb3d."""

class Expression:

    def __str__(self):
        raise NotImplementedError()

class IntVal(Expression):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Variable(Expression):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class BinaryOp(Expression):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return '({left} {op} {right})'.format(left=self.left, right=self.right,
                                              op=self.op)

class UnaryOp(Expression):

    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    def __str__(self):
        return '{op}{arg}'.format(op=self.op, arg=self.arg)

class Assign(Expression):

    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __str__(self):
        return '{var} = {expr}'.format(var=self.var, expr=self.expr)

class CallFunc(Expression):

    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        args = ', '.join(str(expr) for expr in self.args)
        return '{func}({args})'.format(func=self.func, args=args)

class Sequence(Expression):

    def __init__(self, *args, **kwds):
        self.list = list(*args, **kwds)

    def copy(self):
        result = Sequence()
        result.list = self.list.copy()

        return result

    def append(self, value):
        return self.list.append(value)

    def __str__(self):
        result = ''
        for elem in self.list:
            result += str(elem) + '\n'
        return result
