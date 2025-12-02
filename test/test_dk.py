""" """

import inspect
import sys

import pytest

from deprecate_kwargs import deprecate_kwargs
from deprecate_kwargs._dk import _WARNING_CATEGORY


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
        assert str(some_func.__signature__) == "(new_arg_1:int, new_arg_2:int, *, new_kw:int=3)"  # type: ignore
    else:
        assert str(some_func.__signature__) == "(new_arg_1: int, new_arg_2: int, *, new_kw: int = 3)"  # type: ignore
    assert some_func(10, 20, new_kw=4) == 120  # type: ignore
    expected_some_doc = (
        "Let's use this function to test the decorator."
        "\n\nParameters\n----------"
        "\nnew_arg_1 : int\n    Argument 1."
        "\n\n    .. versionchanged:: 0.1.0"
        "\nnew_arg_2 : int\n    Argument 2."
        "\n\n    .. versionchanged:: 0.1.0"
        "\nnew_kw : int, default 3\n    Keyword argument."
        "\n\n    .. versionchanged:: 0.1.0"
        "\n\nReturns\n-------\nint\n    The result of the calculation."
        "\n"
    )
    assert inspect.cleandoc(some_func.__doc__) == inspect.cleandoc(expected_some_doc)  # type: ignore

    pytest.warns(_WARNING_CATEGORY, some_func, old_arg_1=10, old_arg_2=20, old_kw=3)

    expected_another_doc = (
        "Let's use another function to test the decorator."
        "\n\nParameters\n----------"
        "\nnew_arg_1 : int\n    Argument 1."
        "\n\n    .. versionchanged:: 0.1.0"
        "\nnew_arg_2 : int\n    Argument 2."
        "\n\n    .. versionchanged:: 0.1.0"
        "\nkw_new_again : int, default 3\n    Keyword argument."
        "\n\n    .. versionchanged:: 0.1.0"
        "\n\n    .. versionchanged:: 0.3.0"
        "\n"
    )
    assert inspect.cleandoc(another_func.__doc__) == inspect.cleandoc(expected_another_doc)  # type: ignore

    expected_yet_doc = (
        "Let's try another function."
        "\n\nThis time we don't specify a version."
        "\n\nParameters\n----------"
        "\nnew_arg_1 : int\n    Argument 1."
        "\nnew_arg_2 : int\n    Argument 2."
        "\nnew_kw : int, default 3\n    Keyword argument."
        "\n"
    )
    assert inspect.cleandoc(yet_another_func.__doc__) == inspect.cleandoc(expected_yet_doc)  # type: ignore


def test_dk_missing_param_in_docstring():
    """
    Test the case where the argument to be deprecated exists in the signature
    but is NOT mentioned in the docstring.
    """

    @deprecate_kwargs([["new_missing", "old_missing"]], version="0.1.0")
    def func_undocumented_param(old_missing: int):
        """
        This function has a parameter but does not document it.

        Returns
        -------
        int
            Something.
        """
        return old_missing

    sig = str(inspect.signature(func_undocumented_param))
    assert "new_missing" in sig
    assert "old_missing" not in sig

    doc = func_undocumented_param.__doc__
    assert "versionchanged" not in doc  # type: ignore

    assert func_undocumented_param(new_missing=5) == 5  # type: ignore
