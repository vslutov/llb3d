# -*- coding: utf-8 -*-

"""Context for llb3d compiler.

Global and local Blitz objects.
"""

import threading

class Context:

    """Context for global and local objects."""

    def __init__(self):
        """See help(type(obj))."""
        self.functions = {}
        self.globals = {}

_CURRENT_CONTEXT = threading.local()

class ContextProvider:

    """Context provider.

    Should use with current_context proxy:

    >>> context = Context()
    >>> with ContextProvider(context):
    >>>     with current_context() as inner_context:
    >>>         assert current_context() is context
    """

    def __init__(self, context: Context):
        """See help(type(obj))."""
        self.context = context
        self.prev_context = None

    def __enter__(self):
        """See help(type(obj))."""
        self.prev_context = getattr(_CURRENT_CONTEXT, 'context', None)
        _CURRENT_CONTEXT.context = self.context

    def __exit__(self, exception_type, exception_value, traceback):
        """See help(type(obj))."""
        _CURRENT_CONTEXT.context = self.prev_context

class ContextProxy:

    """Context provider proxy.

    Should use with ContextProvider:

    >>> context = Context()
    >>> with ContextProvider(context):
    >>>     with current_context() as inner_context:
    >>>         assert current_context() is context
    """

    def __enter__(self):
        """See help(type(obj))."""
        return getattr(_CURRENT_CONTEXT, 'context', None)

    def __exit__(self, exception_type, exception_value, traceback):
        """See help(type(obj))."""

def current_context():
    """Get current context manager.

    Should use with ContextProvider:
    >>> context = Context()
    >>> with ContextProvider(context):
    >>>     with current_context() as inner_context:
    >>>         assert current_context() is context
    """
    return ContextProxy()
