"""
"""

import sys

try:
    from deprecate_kwargs import deprecate_kwargs
except ModuleNotFoundError:
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).absolute().parents[1]))

    from deprecate_kwargs import deprecate_kwargs


@deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"]])
def some_func(old_arg_1: int, old_arg_2: int):
    """
    Parameters
    ----------
    old_arg_1: int,
        argument 1
    old_arg_2: int,
        argument 2

    """
    return old_arg_1 + old_arg_2


def test_dk():
    """ """

    if sys.version_info[:2] <= (3, 6):
        assert str(some_func.__signature__) == "(new_arg_1:int, new_arg_2:int)"
    else:
        assert str(some_func.__signature__) == "(new_arg_1: int, new_arg_2: int)"
    assert some_func(10, 20) == 30
    assert (
        some_func.__doc__
        == "\n    Parameters\n    ----------\n    new_arg_1: int,\n        argument 1\n    new_arg_2: int,\n        argument 2\n\n    "
    )


if __name__ == "__main__":
    test_dk()
