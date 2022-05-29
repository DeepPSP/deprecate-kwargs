"""
"""

import inspect
import warnings
from copy import deepcopy
from functools import wraps
from typing import Sequence, Callable


__all__ = [
    "deprecate_kwargs",
]


def deprecate_kwargs(l_kwargs: Sequence[Sequence[str]]) -> Callable:
    """

    Decorator to deprecate old kwargs in a function,
    with signature and docstring modified accordingly.
    Instead of replacing the old kwargs with new ones,
    this decorator makes old and new kwargs both available,
    with warnings raised when old kwargs are passed.

    Parameters
    ----------
    l_kwargs: Sequence[Sequence[str]],
        a list of kwargs to be deprecated,
        each element is a sequence of length 2,
        of the form (new_kwarg, old_kwarg)

    Examples
    --------
    >>> @deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"]])
    >>> def some_func(old_arg_1: int, old_arg_2: int):
    >>>     return old_arg_1 + old_arg_2
    >>> some_func.__signature__
    <Signature (new_arg_1:int, new_arg_2:int)>
    >>> some_func(10, 20)
    30
    >>> some_func(new_arg_1=10, new_arg_2=20)
    30
    >>> some_func(old_arg_1=10, old_arg_2=20)
    UserWarning: key word argument "old_arg_1" is deprecated, use "new_arg_1" instead
    UserWarning: key word argument "old_arg_2" is deprecated, use "new_arg_2" instead
    30

    """

    def decorator(func: Callable) -> Callable:
        """ """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            """ """
            old_kwargs = deepcopy(kwargs)
            for new_kw, old_kw in l_kwargs:
                if new_kw in kwargs:
                    old_kwargs.pop(new_kw, None)
                    old_kwargs[old_kw] = kwargs[new_kw]
                elif old_kw in kwargs:
                    warnings.warn(
                        f"key word argument \042{old_kw}\042 is deprecated, use \042{new_kw}\042 instead"
                    )
            return func(*args, **old_kwargs)

        func_params = list(inspect.signature(func).parameters.values())
        func_param_names = list(inspect.signature(func).parameters.keys())
        wrapper.__doc__ = deepcopy(func.__doc__)
        for new_kw, old_kw in l_kwargs:
            idx = func_param_names.index(old_kw)
            func_params[idx] = func_params[idx].replace(name=new_kw)
            if wrapper.__doc__ is not None:
                wrapper.__doc__ = wrapper.__doc__.replace(old_kw, new_kw)
        wrapper.__signature__ = inspect.Signature(parameters=func_params)
        return wrapper

    return decorator
