# -*- coding: utf-8 -*-

"""Test case for backend."""

from .. import backend
from llvmlite import ir, binding

def test_types():
    """Check that we have types."""
    assert isinstance(backend.int8_t, ir.IntType)
    assert isinstance(backend.int32_t, ir.IntType)
    assert isinstance(backend.p_int8_t, ir.PointerType)
    assert isinstance(backend.void_t, ir.VoidType)

def test_init_backend():
    """Check that after init builder and runtime is available."""
    _backend = backend.Backend()
    assert isinstance(_backend.source_module, ir.Module)
    assert isinstance(_backend.runtime, dict)
    assert isinstance(_backend.builder, ir.IRBuilder)

def test_emit_assembly():
    """Check that in assembler remains bbmain."""
    _backend = backend.Backend()
    asm = _backend.emit_assembly()
    assert 'bbmain' in asm

def test_emit_executable(tmpdir):
    """Check that we can create empty executable."""
    _backend = backend.Backend()

    output = tmpdir.join('output')
    _backend.emit_executable(output)
    output.check(file=1, exists=1)
    assert output.sysexec() == ''
