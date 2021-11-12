import re
from pathlib import Path

from setuptools import Extension, setup

ROOT = Path(__file__).parent

CFLAGS = ["-O2"]
# CFLAGS = ["-O0", "-g", "-Wall"]

with open(ROOT / "pysegmenttree" / "__init__.py") as fp:
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


extensions = [
    Extension(
        "pysegmenttree.c_extensions",
        [
            "pysegmenttree/c_extensions.c",
        ],
        extra_compile_args=CFLAGS,
    ),
]

setup(
    name="pysegmenttree",
    version=version,
    url="https://github.com/greshilov/pysegmenttree.git",
    author="Viacheslav Greshilov",
    author_email="s@greshilov.me",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
    license_files=("LICENSE.txt",),
    description="Segment Tree for python 3+",
    long_description=(ROOT / "README.md").read_text().strip(),
    long_description_content_type="text/markdown",
    keywords=["segment", "tree", "range", "segment tree"],
    packages=["pysegmenttree"],
    python_requires=">=3.6",
    include_package_data=True,
    ext_modules=extensions,
)
