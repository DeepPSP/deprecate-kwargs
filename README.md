# [deprecate-kwargs](https://github.com/DeepPSP/deprecate-kwargs/)

[![formatting](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/check-formatting.yml/badge.svg)](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/check-formatting.yml)
[![pytest](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/run-pytest.yml/badge.svg)](https://github.com/DeepPSP/deprecate-kwargs/actions/workflows/run-pytest.yml)
[![codecov](https://codecov.io/gh/DeepPSP/deprecate-kwargs/branch/master/graph/badge.svg?token=6J4Q7SBF7M)](https://codecov.io/gh/DeepPSP/deprecate-kwargs)
[![PyPI](https://img.shields.io/pypi/v/deprecate-kwargs?style=flat-square)](https://pypi.org/project/deprecate-kwargs/)
[![downloads](https://img.shields.io/pypi/dm/deprecate-kwargs?style=flat-square)](https://pypistats.org/packages/deprecate-kwargs)
[![license](https://img.shields.io/github/license/DeepPSP/deprecate-kwargs?style=flat-square)](LICENSE)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/DeepPSP/deprecate-kwargs)
![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/DeepPSP/deprecate-kwargs/latest)

A Tool for Deprecating (Keyword) Arguments for Backward Compatibility for Python Functions.

A decorator is implemented to deprecate old kwargs in a function, with signature and docstring modified accordingly.
Instead of replacing the old kwargs with new ones, this decorator makes old and new kwargs both available,
with warnings raised when old kwargs are passed.

<!-- toc -->

- [deprecate-kwargs](#deprecate-kwargs)
  - [Installation](#installation)
  - [Usage Example](#usage-example)
  - [Benefits](#benefits)

<!-- tocstop -->

## Installation

Run

```bash
python -m pip install deprecate-kwargs
```

or install the latest version in [GitHub](https://github.com/DeepPSP/deprecate-kwargs/) using

```bash
python -m pip install git+https://github.com/DeepPSP/deprecate-kwargs.git
```

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
>>> some_func(10, old_arg_2=20, old_kw=3)
PendingDeprecationWarning: (keyword) argument "old_arg_2" is deprecated, use "new_arg_2" instead
PendingDeprecationWarning: (keyword) argument "old_kw" is deprecated, use "new_kw" instead
90
```

## Benefits

`deprecate_kwargs` is quite useful when one wants to change the name of an argument (or keyword argument) of some function, while keeping old codes using this function still working, hence is beneficial for backward compatibility. For example, say in version 0.1 of some package, there's a function

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
