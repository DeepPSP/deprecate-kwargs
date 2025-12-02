""" """

import inspect
import warnings
from copy import deepcopy
from functools import wraps
from typing import Callable, Optional, Sequence

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
        def wrapper(*args, **kwargs):
            input_kwargs = deepcopy(kwargs)
            for new_kw, old_kw in l_kwargs:
                if new_kw in kwargs:
                    input_kwargs.pop(new_kw, None)
                    input_kwargs[old_kw] = kwargs[new_kw]
                elif old_kw in kwargs:
                    warnings.warn(
                        f'(keyword) argument "{old_kw}" is deprecated, use "{new_kw}" instead',
                        _WARNING_CATEGORY,
                    )
            return func(*args, **input_kwargs)

        func_params = list(inspect.signature(func).parameters.values())
        func_param_names = list(inspect.signature(func).parameters.keys())

        # Normalize docstring (dedented) as the canonical form to edit
        orig_doc = func.__doc__
        doc = inspect.cleandoc(orig_doc) if orig_doc is not None else None

        for new_kw, old_kw in l_kwargs:
            # rename parameters in signature
            idx = func_param_names.index(old_kw)
            func_params[idx] = func_params[idx].replace(name=new_kw)
            func_param_names[idx] = new_kw
            # replace occurrences in dedented docstring
            if update_docstring and doc is not None:
                doc = doc.replace(old_kw, new_kw)

        if version is not None and update_docstring and doc is not None:
            for new_kw, _ in l_kwargs:
                lines = doc.splitlines()
                n = len(lines)
                start_idx = None
                # find the first top-level line that startswith the parameter name
                for i, line in enumerate(lines):
                    if line.strip().startswith(new_kw) and (len(line) - len(line.lstrip()) == 0):
                        start_idx = i
                        break
                if start_idx is None:
                    # fallback: couldn't find the param name — skip
                    continue
                # find j: the index of next top-level line after the param block
                j = start_idx + 1
                while j < n:
                    line = lines[j]
                    indent = len(line) - len(line.lstrip())
                    if indent == 0 and line.strip() != "":
                        break
                    j += 1

                directive = "    .. versionchanged:: " + version
                insert_block = []
                if j > 0 and lines[j - 1].strip() != "":
                    insert_block.append("")
                insert_block.append(directive)
                # Determine whether we need a trailing blank line after the directive
                need_trailing_blank = True
                if j < len(lines):
                    next_line = lines[j].strip()
                    parts = next_line.split(":")[0].strip().lstrip("*").split()
                    candidate_name = parts[0] if parts else ""

                    if candidate_name in func_param_names:
                        need_trailing_blank = False
                else:
                    need_trailing_blank = False

                if need_trailing_blank and j < len(lines):
                    insert_block.append("")

                lines = lines[:j] + insert_block + lines[j:]
                doc = "\n".join(lines)

        wrapper.__doc__ = doc
        wrapper.__signature__ = inspect.Signature(parameters=func_params)
        return wrapper

    warnings.simplefilter("default")

    return decorator
