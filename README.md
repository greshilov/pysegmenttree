# pysegmenttree
Segment tree is a data structure to store information about intervals and perform efficient queries on them.

Properties of the segment tree with the size N.

| Operation | Time complexity |
| --------------- | --------------- |
| build | O(N) |
| query | O(Log[N]) |
| update | O(Log[N]) |

# Key features
* Implements classical data structure to deal with interval queries.
* Includes two classes **IntSegmentTree** and **FloatSegmentTree** implemented in pure C. They can boost performance up to 20x and are used by default for simple data types if possible.

# Installation
```
$ pip install pysegmenttree
```

# Basic usage
```
>> from pysegmenttree import stree

# Build the tree
>> tree = stree([5, 1, 9, 4, 5, 11])

# Find sum on the interval [1, 4)
>> tree.query(1, 4)
14

# Set element with index 3 to 6
>> tree.update(3, 6)
>> tree.query(1, 4)
16
```

# Development

## Insall dependencies
```
pip install -r requirements.dev.txt
pip install -e .
```
## Lock dependencies
```
pip-compile requirements.dev.in
```

## Test
```
pytest -v
```

## Benchmark
```
python benchmarks/benchmark.py
```
