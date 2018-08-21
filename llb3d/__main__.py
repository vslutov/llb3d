# -*- coding: utf-8 -*-

"""llb3d - LLVM Blitz3d implementation."""

import argparse

from . import __version__

def main():
    """Execute, when user call llb3d."""
    parser = argparse.ArgumentParser(description='llb3d ' + __version__)

    parser.add_subparsers(title='commands',
                          help='commands for compiler')

    args = parser.parse_args()

    if 'func' not in args:
        parser.print_help()
    else:
        args.func(args)
