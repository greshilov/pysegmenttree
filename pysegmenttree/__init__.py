
try:
    from ._pysegmenttree import (
        system
    )
except ImportError:  # pragma: no cover
    from ._pysegmenttree_py import (
        system
    )
