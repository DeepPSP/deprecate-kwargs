""" """

import sys

import pytest

from deprecate_kwargs import deprecate_kwargs
from deprecate_kwargs._dk import _WARNING_CATEGORY, _find_indent


@deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"], ["new_kw", "old_kw"]], version="0.1.0")
def some_func(old_arg_1: int, old_arg_2: int, *, old_kw: int = 3) -> int:
    """Let's use this function to test the decorator.

    Parameters
    ----------
    old_arg_1 : int
        Argument 1.
    old_arg_2 : int
        Argument 2.
    old_kw : int, default 3
        Keyword argument.

    Returns
    -------
    int
        The result of the calculation.

    """
    return (old_arg_1 + old_arg_2) * old_kw


@deprecate_kwargs([["kw_new_again", "new_kw"]], version="0.3.0")
@deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"], ["new_kw", "old_kw"]], version="0.1.0")
def another_func(old_arg_1: int, old_arg_2: int, *, old_kw: int = 3) -> None:
    """
    Let's use another function to test the decorator.

    Parameters
    ----------
    old_arg_1 : int
        Argument 1.
    old_arg_2 : int
        Argument 2.
    old_kw : int, default 3
        Keyword argument.

    """
    print(old_arg_1, old_arg_2, old_kw)


@deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"], ["new_kw", "old_kw"]])
def yet_another_func(old_arg_1: int, old_arg_2: int, *, old_kw: int = 3) -> None:
    """Let's try another function.

    This time we don't specify a version.

    Parameters
    ----------
    old_arg_1 : int
        Argument 1.
    old_arg_2 : int
        Argument 2.
    old_kw : int, default 3
        Keyword argument.

    """
    print(old_arg_1, old_arg_2, old_kw)


def test_dk():
    """Test the deprecate_kwargs decorator."""

    if sys.version_info[:2] <= (3, 6):
        assert str(some_func.__signature__) == "(new_arg_1:int, new_arg_2:int, *, new_kw:int=3)"
    else:
        assert str(some_func.__signature__) == "(new_arg_1: int, new_arg_2: int, *, new_kw: int = 3)"
    assert some_func(10, 20, new_kw=4) == 120
    assert some_func.__doc__ == (
        "Let's use this function to test the decorator."
        "\n\n    Parameters\n    ----------"
        "\n    new_arg_1 : int\n        Argument 1."
        "\n\n        .. versionchanged:: 0.1.0"
        "\n    new_arg_2 : int\n        Argument 2."
        "\n\n        .. versionchanged:: 0.1.0"
        "\n    new_kw : int, default 3\n        Keyword argument."
        "\n\n        .. versionchanged:: 0.1.0"
        "\n\n    Returns\n    -------\n    int\n        The result of the calculation."
        "\n\n    "
    )

    pytest.warns(_WARNING_CATEGORY, some_func, old_arg_1=10, old_arg_2=20, old_kw=3)

    assert another_func.__doc__ == (
        "\n    Let's use another function to test the decorator."
        "\n\n    Parameters\n    ----------"
        "\n    new_arg_1 : int\n        Argument 1."
        "\n\n        .. versionchanged:: 0.1.0"
        "\n    new_arg_2 : int\n        Argument 2."
        "\n\n        .. versionchanged:: 0.1.0"
        "\n    kw_new_again : int, default 3\n        Keyword argument."
        "\n\n        .. versionchanged:: 0.1.0"
        "\n\n        .. versionchanged:: 0.3.0"
        "\n\n    "
    )

    assert yet_another_func.__doc__ == (
        "Let's try another function."
        "\n\n    This time we don't specify a version."
        "\n\n    Parameters\n    ----------"
        "\n    new_arg_1 : int\n        Argument 1."
        "\n    new_arg_2 : int\n        Argument 2."
        "\n    new_kw : int, default 3\n        Keyword argument."
        "\n\n    "
    )


def test_find_indent():
    """Test the _find_indent function."""

    assert _find_indent(None) == (0, 4)
    assert _find_indent("") == (0, 4)
    assert _find_indent("    ") == (0, 4)
    assert _find_indent("        ") == (0, 4)
    assert _find_indent("  a") == (2, 2)
    assert _find_indent("   a") == (3, 3)
    assert _find_indent("   a\n") == (0, 4)
    assert _find_indent(some_func.__doc__) == (4, 4)
    assert _find_indent(another_func.__doc__) == (4, 4)
