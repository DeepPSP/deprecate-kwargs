# [deprecate-kwargs](https://github.com/DeepPSP/deprecate-kwargs/)

![formatting](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/check-formatting.yml/badge.svg)
![pytest](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/run-pytest.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/deprecate-kwargs?style=flat-square)

A Tool for Depreating (Keyword) Arguments for Python Functions.

A decorator is implemented to deprecate old kwargs in a function, with signature and docstring modified accordingly.
Instead of replacing the old kwargs with new ones, this decorator makes old and new kwargs both available,
with warnings raised when old kwargs are passed.

## Usage Example
```python
>>> from deprecate_kwargs import deprecate_kwargs
>>> @deprecate_kwargs([["new_arg_1", "old_arg_1"], ["new_arg_2", "old_arg_2"], ["new_kw", "old_kw"]])
>>> def some_func(old_arg_1: int, old_arg_2: int, old_kw: int = 3):
>>>     return (old_arg_1 + old_arg_2) * old_kw
>>> some_func.__signature__
<Signature (new_arg_1: int, new_arg_2: int, new_kw: int = 3)>
>>> some_func(10, 20, 3)
90
>>> some_func(new_arg_1=10, new_arg_2=20, new_kw=3)
90
>>> some_func(old_arg_1=10, old_arg_2=20, old_kw=3)
UserWarning: key word argument "old_arg_1" is deprecated, use "new_arg_1" instead
UserWarning: key word argument "old_arg_2" is deprecated, use "new_arg_2" instead
UserWarning: key word argument "old_kw" is deprecated, use "new_kw" instead
90
```

`deprecate_kwargs` is quite useful when one wants to change the name of an argument (or keyword argument) of some function, while keeping old codes using this function still working. For example, say in version 0.1 of some package, there's a function
```python
def some_deep_learning_model_trainer(learning_rate, ...):
    ...
```
And in version 0.2, someone wants to change `learning_rate` to `lr`. If it was replaced directly via
```python
def some_deep_learning_model_trainer(lr, ...):
    ...
```
then old codes using this function bycalling `some_deep_learning_model_trainer(learning_rate=1e-3, ...)` would break. However, if the replacement is done using
```python
@deprecate_kwargs([["lr", "learning_rate"]])
def some_deep_learning_model_trainer(learning_rate, ...):
    ...
```
then one can call this function using `some_deep_learning_model_trainer(lr=1e-3)`, as well as `some_deep_learning_model_trainer(learning_rate=1e-3, ...)` only with a warning raised. In this way, old codes are rescued from breaking.
