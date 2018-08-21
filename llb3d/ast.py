# -*- coding: utf-8 -*-

"""Ast for llb3d."""

from functools import wraps
import collections

IDENT = 2

class FrozenDict(collections.Mapping):
    """Frozen dict."""

    def __init__(self, *args, **kwargs):
        self.dict = dict(*args, **kwargs)

        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems())))
        # so far, but this solution is O(n).
        self.hash = 0
        for pair in self.items():
            self.hash ^= hash(pair)

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __getitem__(self, key):
        return self.dict[key]

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        if type(self) is not type(other) or hash(self) != hash(other):
            return False
        else:
            return self.dict == other.dict

def is_function(obj):
    """Test, can we call an obj."""
    try:
        getattr(obj, '__call__')
        return True
    except AttributeError:
        return False

class Expression(FrozenDict):

    """Basic expression."""

    def __init__(self, format_str, *args, **kwds):
        super().__init__(*args, **kwds)
        self.hash ^= hash(format_str)
        self.format_str = format_str

    def __str__(self):
        return self.format_str.format(**self)

class IntVal(Expression):

    """Integer."""

    def __init__(self, value):
        super().__init__('{value}', value=value)

class Variable(Expression):

    """Variable."""

    def __init__(self, name):
        super().__init__('{name}', name=name)

class BinaryOp(Expression):

    """Binary operator."""

    def __init__(self, op, left, right):
        super().__init__('({left} {op} {right})', left=left, op=op, right=right)

class UnaryOp(Expression):

    """Unary operator."""

    def __init__(self, op, expr):
        super().__init__('{op} {expr}', op=op, expr=expr)

class Assign(Expression):

    """Assign operator."""

    def __init__(self, var, expr):
        super().__init__('{var} = {expr}', var=var, expr=expr)

class Sequence(Expression):

    """Sequence of operators or expressions."""

    def __init__(self, *args):
        super().__init__(None, tuple=tuple(args))

    def __getattr__(self, name):
        res = getattr(self['tuple'], name)

        if is_function(res):

            @wraps(res)
            def wrapper(*args, **kwds):
                """If result is tuple, we should return elem with right type."""
                result = res(*args, **kwds)
                if isinstance(result, tuple):
                    return type(self)(*result)
                else:
                    return result

            return wrapper

        else:
            return res

    def __iter__(self):
        return iter(self.dict['tuple'])

    def __len__(self):
        return len(self.dict['tuple'])

    def __getitem__(self, key):
        return self.dict['tuple'][key]

    def append(self, value):
        """Append value and return result."""
        return type(self)(*self, value)

    def __str__(self):
        raise NotImplementedError()

class OperatorSequence(Sequence):
    """Operator sequence."""
    def __str__(self):
        return '\n'.join(str(elem) for elem in self['tuple'])

class ExpressionSequence(Sequence):
    """Expression sequence."""
    def __str__(self):
        return ', '.join(str(elem) for elem in self['tuple'])

class Ident(OperatorSequence):

    """Identation operator sequence."""

    def __init__(self, sequence):
        super().__init__(*sequence)

    def __str__(self):
        body = super().__str__().split('\n')
        return '\n'.join(' ' * IDENT + line for line in body)

class If(Expression):

    """If expression."""

    def __init__(self, expr, true_branch, false_branch):
        super().__init__('IF {expr}\n{true_branch}\nELSE\n{false_branch}\nENDIF',
                         expr=expr, true_branch=true_branch,
                         false_branch=false_branch)

    def __str__(self):
        if len(self['false_branch']) == 0:
            return 'IF {expr}\n{true_branch}\nENDIF'.format(*self)
        else:
            return super().__str__()

class FuncDef(Expression):

    """Function definition."""

    def __init__(self, name, args, body):
        super().__init__('FUNCTION {name}({args})\n{body}\nEND FUNCTION',
                         name=name, args=args, body=body)

class FuncCall(Expression):

    """Function call."""

    def __init__(self, name, args):
        super().__init__('{name}({args})', name=name, args=args)

class ProcCall(Expression):

    """Procedure call."""

    def __init__(self, name, args):
        super().__init__('{name} {args}', name=name, args=args)
