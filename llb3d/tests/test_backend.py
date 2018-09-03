# -*- coding: utf-8 -*-

"""Test case for backend."""

from ..backend import Backend
from llvmlite import ir, binding

def test_types():
    """Check that we have types."""
    backend = Backend()
    assert isinstance(backend.int8_t, ir.IntType)
    assert isinstance(backend.cstr_t, ir.PointerType)
    assert isinstance(backend.int32_t, ir.IntType)
    assert isinstance(backend.float32_t, ir.FloatType)
    assert isinstance(backend.void_t, ir.VoidType)

def test_init_backend():
    """Check that after init builder and runtime is available."""
    backend = Backend()
    assert isinstance(backend.source_module, ir.Module)
    assert isinstance(backend.runtime, dict)
    assert isinstance(backend.builder, ir.IRBuilder)

def test_emit_assembly():
    """Check that in assembler remains bbmain."""
    backend = Backend()
    asm = backend.emit_assembly()
    assert 'bbmain' in asm

def test_emit_executable(tmpdir):
    """Check that we can create empty executable."""
    backend = Backend()

    output = tmpdir.join('output')
    backend.emit_executable(output)
    output.check(file=1, exists=1)
    assert output.sysexec() == ''
