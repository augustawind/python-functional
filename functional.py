'''Decorators for more functional functions.'''
from collections import deque
from inspect import signature
from itertools import islice


# Curried function decorator.
def curried(function, _nargs=0, _args=(), _kwargs={}):
    args_needed = len(signature(function.__call__).parameters)

    def curried_function(*args, **kwargs):
        nargs = _nargs + len(args) + len(kwargs)
        args += _args
        kwargs.update(_kwargs)

        if nargs >= args_needed:
            return function(*args, **kwargs)
        else:
            return curried(function, nargs, args, kwargs)

    return curried_function


# Curried function decorator implemented with classes.
class CurriedFunction():

    def __init__(self, function, nargs=0, args=(), kwargs={}):
        self.function = function
        self.args_needed = len(signature(function.__call__).parameters)
        self.nargs = nargs
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        nargs = self.nargs + len(args) + len(kwargs)
        args += self.args
        kwargs.update(self.kwargs)

        self.__init__(self.function)

        if nargs >= self.args_needed:
            return self.function(*args, **kwargs)
        else:
            return CurriedFunction(self.function, nargs, args, kwargs)


# Composable functions with the * operator
class Composable():

    def __init__(self, *functions):
        self.initial = functions
        self.functions = deque(functions)

    def __mul__(self, function):
        self.functions.appendleft(function)
        composable = Composable(*self.functions)
        self.functions = deque(self.initial)
        return composable

    def __call__(self, *args, **kwargs):
        val = self.functions[0](*args, **kwargs)

        for f in islice(self.functions, 1, None):
            val = f(val)

        return val
