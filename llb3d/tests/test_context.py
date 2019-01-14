# -*- coding: utf-8 -*-

"""Test case for backend."""

from pytest import raises

from ..context import Context, ContextProvider, current_context

def test_empty_context():
    """Check that context have functions and globals."""
    context = Context()
    assert context.functions == {}
    assert context.globals == {}

def test_empty_context_provider():
    """Current context should be None by default."""
    with current_context() as context:
        assert context is None

def test_simple_context_provider():
    """Check that context provider works with current_context proxy."""
    context = Context()

    with ContextProvider(context):
        with current_context() as inner_context:
            assert inner_context is context

def test_exception():
    """Check that context provider throws exceptions."""
    context = Context()

    with raises(RuntimeError):
        with ContextProvider(context):
            with current_context():
                raise RuntimeError('simple error')

def test_recursive():
    """Check that context provider can be recursive."""
    context1 = Context()
    context2 = Context()

    with ContextProvider(context1):
        with current_context() as inner_context1:
            assert context1 is inner_context1

        with ContextProvider(context2):
            with current_context() as inner_context2:
                assert context2 is inner_context2

        with current_context() as inner_context3:
            assert context1 is inner_context3
