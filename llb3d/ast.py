# -*- coding: utf-8 -*-

"""Ast for llb3d."""

import collections
from typing import Tuple
from textwrap import indent
from inspect import signature

from typeguard import typechecked

IDENT = 2

class FrozenDict(collections.Mapping):
    """Frozen dict."""

    def __init__(self, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        self._dict = dict(**kwargs)

        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems())))
        # so far, but this solution is O(n).
        self._hash = 0
        for pair in self.items():
            self._hash ^= hash(pair)

    def __iter__(self):
        """Implement iter(self)."""
        return iter(self._dict)

    def __len__(self) -> int:
        """Implement len(self)."""
        return len(self._dict)

    def __getitem__(self, key):
        """Implement self[key]."""
        return self._dict[key]

    def __hash__(self) -> int:
        """Implement hash(self)."""
        return self._hash

    def __eq__(self, other) -> bool:
        """Return self==other."""
        if type(self) is not type(other) or hash(self) != hash(other):
            return False

        #pylint: disable=protected-access
        return self._dict == other._dict

    @typechecked
    def __getattr__(self, name: str):
        """Return name from dict."""
        return self._dict[name]

class Statement(FrozenDict):
    """Basic statement.

    Frozen dict, that can be printed.

    >>> expr = Statement("Hello, {name}!", name='Alice')
    >>> expr['name']
    'Alice'
    >>> str(expr)
    'Hello, Alice!'
    """

    def __init__(self, format_str, **kwds):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(**kwds)
        self._hash ^= hash(format_str) ^ hash(type(self))
        self._format_str = format_str

    def __str__(self) -> str:
        """Implement str(self)."""
        return self._format_str.format(**self)

    def __repr__(self) -> str:
        """Implemet repr(self)."""
        sig = signature(type(self).__init__)
        params = tuple(sig.parameters.keys())
        params_str = ', '.join(repr(self[c]) for c in params[1:])
        return ("{cls}({params_str})"
                .format(cls=type(self).__name__, params_str=params_str))

class Expression(Statement):
    """Basic expression."""

class Identifier(Expression):
    """Identifier for variable or function.

    >>> alice = Identifier('Alice')
    >>> alice['name']
    'Alice'
    >>> str(alice)
    'Alice'
    """

    @typechecked
    def __init__(self, name: str):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{name}', name=name)

class Literal(Expression):
    """Abstract literal."""

    def __init__(self, value):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{value}', value=value)

class IntLiteral(Literal):
    """Integer literal.

    Integer values are numeric values with no fractional part in them.
    For example: 5, -10, 0 are integer values.
    All integer values in your program must be in the range -2147483648
    to +2147483647 (int32).
    """

    @typechecked
    def __init__(self, value: int):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)

class FloatLiteral(Literal):
    """Float literal.

    Floating point values are numeric values that include a fractional part.
    For example: .5, -10.1, 0.0 are all floating point values (float32).
    """

    @typechecked
    def __init__(self, value: float):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)

class StrLiteral(Literal):
    """String literal.

    Strings values are used to contain text. For example: "Hello",
    "What's up?", "***** GAME OVER *****", "".
    """

    @typechecked
    def __init__(self, value: str):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)

class UnaryOp(Expression):
    """Unary operator."""

    @typechecked
    def __init__(self, op: str, right: Expression):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{op}{right}', op=op, right=right)

class BinaryOp(Expression):
    """Binary operator."""

    @typechecked
    def __init__(self, op: str, left: Expression, right: Expression):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('({left} {op} {right})', op=op, left=left, right=right)

class ProcedureCall(Statement):
    """Procedure call."""

    @typechecked
    def __init__(self, procedure: Identifier, args: Tuple[Expression, ...]):
        """Initialize self.  See help(type(self)) for accurate signature."""
        args_str = ', '.join(str(arg) for arg in args)
        super().__init__('{procedure} {args_str}', procedure=procedure,
                         args=args, args_str=args_str)

class Body(Statement):
    """Code block.

    For example, global body or function body.
    """

    @typechecked
    def __init__(self, statements: Tuple[Statement, ...]):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('Code block', statements=statements)

    def __str__(self) -> str:
        """Implement str(self)."""
        result = '\n'.join(map(str, self['statements']))
        indented = indent(result, ' ' * IDENT)
        return indented

class Program(Body):
    """Code block without identation."""

    def __str__(self) -> str:
        """Implement str(self)."""
        return '\n'.join(map(str, self['statements']))
