# -*- coding: utf-8 -*-

"""Context for llb3d compiler.

Global variables, functions, etc.
"""

class Context:
    def __init__(self):
        self.functions = {}
        self.globals = {}

_current_context = None

class ContextProvider:
    def __init__(self, context: Context):
        self.context = context
        self.prev_context = None

    def __enter__(self):
        global _current_context
        self.prev_context, _current_context = _current_context, self.context

    def __exit__(self, exception_type, exception_value, traceback):
        global _current_context
        _current_context = self.prev_context

class ContextProxy:
    def __enter__(self):
        global _current_context
        return _current_context

current_context = ContextProxy()
