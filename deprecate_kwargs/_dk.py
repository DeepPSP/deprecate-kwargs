"""
"""

import inspect
import warnings
from copy import deepcopy
from functools import wraps
from typing import Callable, Sequence

__all__ = [
    "deprecate_kwargs",
]


_WARNING_CATEGORY = PendingDeprecationWarning


def deprecate_kwargs(l_kwargs: Sequence[Sequence[str]], update_docstring: bool = True) -> Callable:
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
        for new_kw, old_kw in l_kwargs:
            idx = func_param_names.index(old_kw)
            func_params[idx] = func_params[idx].replace(name=new_kw)
            if update_docstring and wrapper.__doc__ is not None:
                wrapper.__doc__ = wrapper.__doc__.replace(old_kw, new_kw)
        wrapper.__signature__ = inspect.Signature(parameters=func_params)
        return wrapper

    warnings.simplefilter("default")

    return decorator
