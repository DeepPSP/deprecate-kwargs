# [deprecate-kwargs](https://github.com/DeepPSP/deprecate-kwargs/)

![formatting](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/check-formatting.yml/badge.svg)
<!-- ![PyPI](https://img.shields.io/pypi/v/deprecate-kwargs?style=flat-square) -->

A Tool for Depreating (Keyword) Arguments for Python Functions.

A decorator is implemented to deprecate old kwargs in a function, with signature and docstring modified accordingly.
Instead of replacing the old kwargs with new ones, this decorator makes old and new kwargs both available,
with warnings raised when old kwargs are passed.

## Usage Example
```python
>>> from deprecate_kwargs import deprecate_kwargs
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
```
