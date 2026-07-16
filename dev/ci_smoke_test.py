#!/usr/bin/env python
"""
Minimal smoke test executed by cibuildwheel after building a wheel.

The full test suite runs against the built wheels in the dedicated
test_binpy_wheels CI job (one leg per Python version and OS), so this script
only sanity-checks that the wheel imports, that the ctypes layer can load the
bundled FLANN shared library, and that a trivial nearest-neighbor query
round-trips through the C ABI.
"""
import numpy as np


def main():
    import pyflann_ibeis
    from pyflann_ibeis import FLANN, flann_ctypes
    assert flann_ctypes.flannlib is not None, 'failed to load the flann shared library'
    print('pyflann_ibeis {} loaded flann from {}'.format(
        pyflann_ibeis.__version__, flann_ctypes.libpath))

    rng = np.random.RandomState(0)
    dataset = rng.rand(100, 8).astype(np.float32)
    queries = rng.rand(5, 8).astype(np.float32)
    flann = FLANN()
    indexes, dists = flann.nn(dataset, queries, 3, algorithm='kdtree', trees=1)
    assert indexes.shape == (5, 3), 'unexpected result shape {}'.format(indexes.shape)
    assert dists.shape == (5, 3), 'unexpected distance shape {}'.format(dists.shape)
    print('pyflann_ibeis smoke test passed')


if __name__ == '__main__':
    main()
