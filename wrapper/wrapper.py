"""
With this module, we are able to import a function from another namespace into
this namespace, while potentially modifying it too.
"""

import inspect
import moduleA as mA

members = inspect.getmembers(mA, inspect.isfunction)


def modifier_func(f):
    try:
        assert isinstance(f(), str)
        return f
    except AssertionError:
        assert isinstance(f(), int)
        return


def wrap(members):
    for m in members:
        globals()[m[0]] = modifier_func(m[1])


wrap(members)
assert 'functionA' in globals().keys()
assert 'functionB' in globals().keys()
assert callable(functionA)
