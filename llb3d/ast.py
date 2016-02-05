# -*- coding: utf-8 -*-

"""Ast for llb3d."""

class IntVal:

    def __init__(self, value):
        self.value = value

class Variable:

    def __init__(self, name):
        self.name = name

class BinaryOp:

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryOp:

    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

class Assign:

    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class CallFunc:

    def __init__(self, func, args):
        self.func = func
        self.args = args
