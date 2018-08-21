# -*- coding: utf-8 -*-

"""Ast for llb3d."""

import collections

from enforce import runtime_validation

IDENT = 2

class FrozenDict(collections.Mapping):
    """Frozen dict."""

    def __init__(self, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        self.dict = dict(*args, **kwargs)

        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems())))
        # so far, but this solution is O(n).
        self.hash = 0
        for pair in self.items():
            self.hash ^= hash(pair)

    def __iter__(self):
        """Implement iter(self)."""
        return iter(self.dict)

    def __len__(self):
        """Implement len(self)."""
        return len(self.dict)

    def __getitem__(self, key):
        """Implement self[key]."""
        return self.dict[key]

    def __hash__(self):
        """Implement hash(self)."""
        return self.hash

    def __eq__(self, other):
        """Return self==other."""
        if type(self) is not type(other) or hash(self) != hash(other):
            return False

        return self.dict == other.dict

class Expression(FrozenDict):
    """Basic expression.

    Frozen dict, that can be printed.
    >>> expr = Expression("Hello, {name}!", name='Alice')
    >>> expr['name']
    'Alice'
    >>> str(expr)
    'Hello, Alice!'
    """

    def __init__(self, format_str, *args, **kwds):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(*args, **kwds)
        self.hash ^= hash(format_str)
        self.format_str = format_str

    def __str__(self):
        """Implement str(self)."""
        return self.format_str.format(**self)

class Identifier(Expression):
    """Identifier for variable or function.

    >>> alice = Identifier('Alice')
    >>> alice['name']
    'Alice'
    >>> str(alice)
    'Alice'
    """

    def __init__(self, name: str) -> str:
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{name}', name=name)

    def __repr__(self):
        """Implement repr(self).

        >>> print(repr(Identifier('Alice')))
        Identifier('Alice')
        """
        return "{cls}('{name}')".format(cls=type(self).__name__, name=self['name'])

class Literal(Expression):
    """Abstract literal."""

    def __init__(self, value):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{value}', value=value)

    def __repr__(self):
        """Implement repr(self)."""
        return "{cls}({value})".format(cls=type(self).__name__,
                                       value=repr(self['value']))

class IntLiteral(Literal):
    """Integer literal.

    Integer values are numeric values with no fractional part in them.
    For example: 5, -10, 0 are integer values.
    All integer values in your program must be in the range -2147483648
    to +2147483647 (int32).
    """

    @runtime_validation
    def __init__(self, value: int):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)

class FloatLiteral(Literal):
    """Float literal.

    Floating point values are numeric values that include a fractional part.
    For example: .5, -10.1, 0.0 are all floating point values (float32).
    """

    @runtime_validation
    def __init__(self, value: float):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)

class StrLiteral(Literal):
    """String literal.

    Strings values are used to contain text. For example: "Hello",
    "What's up?", "***** GAME OVER *****", "".
    """

    @runtime_validation
    def __init__(self, value: str):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)
