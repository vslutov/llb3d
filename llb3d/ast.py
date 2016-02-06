# -*- coding: utf-8 -*-

"""Ast for llb3d."""

IDENT = 2

class Expression:

    def __str__(self):
        print(type(self))
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
        return '{op} {arg}'.format(op=self.op, arg=self.arg)

class Assign(Expression):

    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __str__(self):
        return '{var} = {expr}'.format(var=self.var, expr=self.expr)

class If(Expression):

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

class DefFunc(Expression):

    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = Ident(body)

    def __str__(self):
        return ('FUNCTION {name}({args})\n{body}\nEND FUNCTION'
                .format(name=self.name, args=self.args, body=self.body))

class CallFunc(Expression):

    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __str__(self):
        return '{func}({args})'.format(func=self.func, args=self.args)

class CallProc(CallFunc):

    def __str__(self):
        return '{func} {args}'.format(func=self.func, args=self.args)

class Sequence(Expression):

    def __init__(self, first=None):
        if first is not None:
            self.list = [first]
        else:
            self.list = []

    def copy(self):
        result = type(self)()
        result.list = self.list.copy()

        return result

    def append(self, value):
        if value is not None:
            self.list.append(value)

    def __len__(self):
        return len(self.list)

class OperatorSequence(Sequence):
    def __str__(self):
        return '\n'.join(str(elem) for elem in self.list)

class ExpressionSequence(Sequence):
    def __str__(self):
        return ', '.join(str(elem) for elem in self.list)

class Ident(OperatorSequence):
    def __init__(self, sequence):
        super().__init__()
        self.list = sequence.list.copy()

    def __str__(self):
        body = super().__str__().split('\n')
        return '\n'.join(' ' * IDENT + line for line in body)
