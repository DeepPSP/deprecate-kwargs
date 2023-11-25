"""
"""

from pathlib import Path

import setuptools

from deprecate_kwargs import __version__

cwd = Path(__file__).absolute().parent

long_description = (cwd / "README.md").read_text(encoding="utf-8")

extras = {}
extras["test"] = [
    "pre-commit",
    "pytest",
    "pytest-xdist",
    "pytest-cov",
]
extras["dev"] = extras["test"]


setuptools.setup(
    name="deprecate_kwargs",
    version=__version__,
    author="DeepPSP",
    author_email="wenh06@gmail.com",
    license="MIT",
    description="A Tool for Deprecating (Keyword) Arguments for Backward Compatibility for Python Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeepPSP/deprecate-kwargs",
    # project_urls={},
    packages=setuptools.find_packages(
        exclude=[
            "docs*",
            "test*",
        ]
    ),
    # entry_points=,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    # install_requires=open("requirements.txt").readlines(),
    extras_require=extras,
)
