# -*- coding: utf-8 -*-

"""llb3d - LLVM Blitz3d implementation"""

import pytest, os, sys, argparse

__version__ = "0.0.1" # Don't forget fix in setup.py

def run_program(args):
    raise NotImplementedError()

def run_debug(args):
    raise NotImplementedError()

def run_compile(args):
    raise NotImplementedError()

def run_tests(args):
    path = os.path.abspath(os.path.dirname(__file__))
    sys.argv[1] = path
    pytest.main()

def main():
    """Execute, when user call modelmachine."""
    parser = argparse.ArgumentParser(description='llb3d ' + __version__)

    subparsers = parser.add_subparsers(title='commands',
                                       help='commands for compiler')

    run = subparsers.add_parser('run', help='run program')
    run.add_argument('filename', help='file with source code')
    run.set_defaults(func=run_program)

    debug = subparsers.add_parser('debug', help='run program in debug mode')
    debug.add_argument('filename', help='file with machine code')
    debug.set_defaults(func=run_debug)

    test = subparsers.add_parser('test', help='run internal tests end exit')
    test.set_defaults(func=run_tests)

    _compile = subparsers.add_parser('compile', help='compile program')
    _compile.add_argument('source_file', help='input file with source')
    _compile.add_argument('dest_file', help='output file')
    _compile.set_defaults(func=run_compile)

    args = parser.parse_args(sys.argv[1:])

    if 'func' not in args:
        parser.print_help()
    else:
        args.func(args)
