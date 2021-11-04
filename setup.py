import re

from distutils.core import setup, Extension
from pathlib import Path


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


args = dict(
    name="pysegmenttree",
    version=version,
    description="Segment Tree for python 3+",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    author="Slava Greshilov",
    author_email="s@greshilov.me",
    packages=["pysegmenttree"],
    python_requires=">=3.6",
    include_package_data=True,
)

setup(
    ext_modules=extensions,
    **args,
)
