#!/usr/bin/env python3

from random import randint


class MyCustomException( Exception ):
    pass

class MyCustomClass:
    def run( self ):
        r = randint(1, 8)
        # NameError
        if r == 1:
            raise NameError
        # ValueError
        if r == 2:
            raise ValueError
        # ZeroDivisionError
        if r == 3:
            raise ZeroDivisionError
        # IndentationError
        if r == 4:
            raise IndentationError
        # OverflowError
        if r == 5:
            raise OverflowError
        # SyntaxError
        if r == 6:
            raise SyntaxError
        # TypeError
        if r == 7:
            raise TypeError
        # MyCustomException
        if r == 8:
            raise MyCustomException


if "__main__" == __name__:
    mc = MyCustomClass()
    mc.run()

# NameError
# ValueError
# ZeroDivisionError
# IndentationError
# OverflowError
# SyntaxError
# TypeError
