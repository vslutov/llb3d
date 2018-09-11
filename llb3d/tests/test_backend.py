# -*- coding: utf-8 -*-

"""Test case for backend."""

import subprocess

from ..backend import Backend
from .. import backend as backend_module
from llvmlite import ir, binding

def test_types():
    """Check that we have types."""
    assert isinstance(backend_module.uchar_t, ir.IntType)
    assert isinstance(backend_module.ustr_t, ir.PointerType)
    assert isinstance(backend_module.int32_t, ir.IntType)
    assert isinstance(backend_module.float32_t, ir.FloatType)
    assert isinstance(backend_module.void_t, ir.VoidType)

def test_init_backend():
    """Check that after init builder and runtime is available."""
    backend = Backend()
    assert isinstance(backend.source_module, ir.Module)
    assert isinstance(backend.runtime, dict)
    assert isinstance(backend.builder, ir.IRBuilder)

def test_optimize():
    """Check that optimize return llvm module."""
    backend = Backend()
    assert isinstance(backend.optimize(), binding.ModuleRef)

def test_emit_llvm():
    """Check that emit_llvm return valid llvm."""
    backend = Backend()
    assert 'bbmain' in backend.emit_llvm()

def test_emit_assembly():
    """Check that in assembler remains bbmain."""
    backend = Backend()
    asm = backend.emit_assembly()
    assert 'bbmain' in asm

def test_run():
    """Check that we can run llvm program."""
    backend = Backend()

    run = backend.run()
    assert isinstance(run, subprocess.CompletedProcess)
    assert run.stdout is None

    run = backend.run(stdout=subprocess.PIPE, encoding='utf-8')
    assert run.stdout == ''

def test_emit_executable(tmpdir):
    """Check that we can create empty executable."""
    backend = Backend()

    output = tmpdir.join('output')
    backend.emit_executable(output)
    output.check(file=1, exists=1)
    assert output.sysexec() == ''
