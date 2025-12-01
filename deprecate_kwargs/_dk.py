""" """

import inspect
import warnings
from copy import deepcopy
from functools import wraps
from typing import Callable, Optional, Sequence, Tuple

__all__ = [
    "deprecate_kwargs",
]


_WARNING_CATEGORY = PendingDeprecationWarning


def deprecate_kwargs(
    l_kwargs: Sequence[Sequence[str]], update_docstring: bool = True, version: Optional[str] = None
) -> Callable:
    """Decorator to deprecate old kwargs in a function,
    with signature and docstring modified accordingly.

    Instead of replacing the old kwargs with new ones,
    this decorator makes old and new kwargs both available,
    with warnings raised when old kwargs are passed.

    Parameters
    ----------
    l_kwargs : Sequence[Sequence[str]]
        A list of kwargs to be deprecated.
        Each element is a sequence of length 2,
        of the form ``(new_kwarg, old_kwarg)``.
    update_docstring : bool, default True
        Whether to update the docstring of the decorated function.
        The update is done by replacing all occurrences of old kwargs
        with new kwargs in the docstring.

        .. versionadded:: 0.0.3
    version : Optional[str], default None
        The version when the kwargs are deprecated.
        If provided, a ``versionchanged`` directive will be added
        to the docstring.

        .. versionadded:: 0.1.0

    Returns
    -------
    Callable
        The decorated function with signature and docstring modified.

    Examples
    --------
    >>> from deprecate_kwargs import deprecate_kwargs
    >>> @deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"], ["new_kw", "old_kw"]])
    >>> def some_func(old_arg_1: int, old_arg_2: int, *, old_kw: int = 3):
    >>>     return (old_arg_1 + old_arg_2) * old_kw
    >>> some_func.__signature__
    <Signature (new_arg_1: int, new_arg_2: int, *, new_kw: int = 3)>
    >>> some_func(10, 20, 3)
    90
    >>> some_func(new_arg_1=10, new_arg_2=20, new_kw=3)
    90
    >>> some_func(10, old_arg_2=20, old_kw=3)
    PendingDeprecationWarning: (keyword) argument "old_arg_2" is deprecated, use "new_arg_2" instead
    PendingDeprecationWarning: (keyword) argument "old_kw" is deprecated, use "new_kw" instead
    90

    Warning
    -------
    If the replaced (old) argument has a simple name, e.g. ``a``,
    then `update_docstring` should better be set to ``False``,
    and the new docstring should be updated manually, or using
    finer-grained methods.

    """
    warnings.simplefilter("always")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            input_kwargs = deepcopy(kwargs)
            for new_kw, old_kw in l_kwargs:
                if new_kw in kwargs:
                    input_kwargs.pop(new_kw, None)
                    input_kwargs[old_kw] = kwargs[new_kw]
                elif old_kw in kwargs:
                    warnings.warn(
                        f"(keyword) argument \042{old_kw}\042 is deprecated, use \042{new_kw}\042 instead",
                        _WARNING_CATEGORY,
                    )
            return func(*args, **input_kwargs)

        func_params = list(inspect.signature(func).parameters.values())
        func_param_names = list(inspect.signature(func).parameters.keys())
        wrapper.__doc__ = deepcopy(func.__doc__)
        doc_indent, unit_indent = _find_indent(wrapper.__doc__)
        for new_kw, old_kw in l_kwargs:
            idx = func_param_names.index(old_kw)
            func_params[idx] = func_params[idx].replace(name=new_kw)
            func_param_names[idx] = new_kw
            if update_docstring and wrapper.__doc__ is not None:
                wrapper.__doc__ = wrapper.__doc__.replace(old_kw, new_kw)
        if version is not None and update_docstring and wrapper.__doc__ is not None:
            # insert versionchanged directive for each deprecated kwarg
            versionchanged = f"\n{' ' * (doc_indent + unit_indent)}.. versionchanged:: {version}"
            for new_kw, _ in l_kwargs:
                lines = wrapper.__doc__.split("\n")
                flag = False
                for idx, line in enumerate(lines):
                    if len(line) - len(line.lstrip()) == doc_indent and line.strip().startswith(new_kw):
                        # the first line of the new kwarg
                        flag = True
                    elif flag and len(line) - len(line.lstrip()) == doc_indent:
                        # the first line of the next kwarg
                        if not any(line.strip().startswith(kw) for kw in func_param_names):
                            # we meet the "Returns" section
                            # or the end of the docstring
                            idx -= 1
                        break
                # insert the versionchanged directive above the next kwarg
                wrapper.__doc__ = "\n".join(lines[:idx] + [versionchanged] + lines[idx:])
        wrapper.__signature__ = inspect.Signature(parameters=func_params)
        return wrapper

    warnings.simplefilter("default")

    return decorator


def _find_indent(docstring: Optional[str] = None) -> Tuple[int, int]:
    """Find the minimum indent of the docstring,
    and the unit indent of the docstring (typically 4).

    Parameters
    ----------
    docstring : str, optional
        The docstring to be processed.

    Returns
    -------
    Tuple[int, int]
        The minimum indent of the docstring,
        and the unit indent of the docstring (typically 4).

    """
    if docstring is None:
        return 0, 4
    # ignore the title line if docstring have multiple lines
    if "\n" in docstring:
        docstring = docstring.split("\n", 1)[-1]
    # ignore empty lines
    lines = filter(None, docstring.split("\n"))
    indents = sorted(set([len(line) - len(line.lstrip()) for line in lines if line.strip()]))
    doc_indent = indents[0] if indents else 0
    if len(indents) > 1:
        unit_indent = min([indents[i] - indents[i - 1] for i in range(1, len(indents))])
    elif doc_indent > 0:
        unit_indent = doc_indent
    else:
        unit_indent = 4
    return doc_indent, unit_indent
