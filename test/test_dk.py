"""
"""

import sys

import pytest

from deprecate_kwargs import deprecate_kwargs
from deprecate_kwargs._dk import _WARNING_CATEGORY


@deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"], ["new_kw", "old_kw"]])
def some_func(old_arg_1: int, old_arg_2: int, *, old_kw: int = 3):
    """
    Parameters
    ----------
    old_arg_1: int,
        argument 1
    old_arg_2: int,
        argument 2
    old_kw: int, default 3,
        keyword argument

    """
    return (old_arg_1 + old_arg_2) * old_kw


def test_dk():
    """ """

    if sys.version_info[:2] <= (3, 6):
        assert str(some_func.__signature__) == "(new_arg_1:int, new_arg_2:int, *, new_kw:int=3)"
    else:
        assert str(some_func.__signature__) == "(new_arg_1: int, new_arg_2: int, *, new_kw: int = 3)"
    assert some_func(10, 20, new_kw=4) == 120
    assert some_func.__doc__ == (
        "\n    Parameters\n    ----------"
        "\n    new_arg_1: int,\n        argument 1"
        "\n    new_arg_2: int,\n        argument 2"
        "\n    new_kw: int, default 3,\n        keyword argument\n\n    "
    )

    pytest.warns(_WARNING_CATEGORY, some_func, old_arg_1=10, old_arg_2=20, old_kw=3)
