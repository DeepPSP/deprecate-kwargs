Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.1.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

`Unreleased <https://github.com/DeepPSP/deprecate-kwargs/compare/v0.1.0...HEAD>`__
-----------------------------------------------------------------------------------

Added
~~~~~

Changed
~~~~~~~

Deprecated
~~~~~~~~~~

Removed
~~~~~~~

Fixed
~~~~~

Security
~~~~~~~~

`0.1.0 <https://github.com/DeepPSP/deprecate-kwargs/compare/v0.0.4...v0.1.0>`__ - 2025-01-27
---------------------------------------------------------------------------------------------

Added
~~~~~

- ``version`` argument to the `deprecate_kwargs` function. This argument
  can be used to specify the version number from which the keyword argument
  is deprecated. This version number will be used to add a versionchanged
  directive in the docstring of the decorated function if the `update_docstring`
  argument is set to True and the docstring of the decorated function is
  a Sphinx-style docstring.
- Changelog file (this file) to the package to keep track of the changes
  in the package.

`0.0.4 <https://github.com/DeepPSP/deprecate-kwargs/compare/v0.0.3...v0.0.4>`__ - 2023-11-26
---------------------------------------------------------------------------------------------

Added
~~~~~

- ``pre-commit`` for code formatting and linting checks.
- Publish to GitHub Release in the CD workflow.

Removed
~~~~~~~

- Removed the script ``push_to_pypi.sh`` to push the package to PyPI.
  As the package is now deployed to PyPI using GitHub Actions,
  no manual deployment is needed.

- Support for Python 3.6.

`0.0.3 <https://github.com/DeepPSP/deprecate-kwargs/compare/v0.0.2...v0.0.3>`__ - 2023-05-04
---------------------------------------------------------------------------------------------

Added
~~~~~

- ``update_docstring`` argument to the `deprecate_kwargs` function.
  This boolean argument can be used as a flag to update the docstring
  (replace the old keyword argument with the new keyword argument) of
  the decorated function.
- CD workflow to deploy the package to PyPI using GitHub Actions.
- Code coverage checks using Codecov in the CI workflow.
- License file to the package.

Changed
~~~~~~~

- Updated the ``README`` file with the latest information about the package.

`0.0.2 <https://github.com/DeepPSP/deprecate-kwargs/releases/tag/v0.0.2>`__ - 2022-06-03
----------------------------------------------------------------------------------------

Added
~~~~~

- The function `deprecate_kwargs` is added to the package. This function
  can be used as a decorator to deprecate keyword arguments in a function.
  Namely, we want to rename a keyword argument in a function, but we want
  to keep the old name for backward compatibility, with a warning message
  to the user. This function can be used to achieve this.
- Demo notebook to demonstrate the usage of the `deprecate_kwargs` function.
- Unit tests for the `deprecate_kwargs` function.
- CI workflow hosted on GitHub Actions.
- Script ``push_to_pypi.sh`` to push the package to PyPI.

0.0.1 [YANKED]
----------------

This release was yanked.
