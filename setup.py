from distutils.core import setup, Extension


CFLAGS = ["-O2"]
extensions = [
    Extension(
        "pysegmenttree._pysegmenttree",
        ["pysegmenttree/_pysegmenttree.c"],
        extra_compile_args=CFLAGS,
    ),
]


args = dict(
    name='pysegmenttree',
    description='Segment Tree for python 3+',
    packages=["pysegmenttree"],
    python_requires=">=3.6",
    include_package_data=True,
)

setup(
    ext_modules=extensions,
    **args,
)
