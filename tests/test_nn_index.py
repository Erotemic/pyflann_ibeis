#!/usr/bin/env python
import pyflann_ibeis
import numpy as np
from numpy import ones
from numpy.random import rand
import pytest
import unittest


class Test_PyFLANN_nn(unittest.TestCase):

    def setUp(self):
        self.nn = pyflann_ibeis.FLANN()


class Test_PyFLANN_nn_index(unittest.TestCase):

    def testnn_index(self):

        dim = 10
        N = 100

        x = rand(N, dim)
        nn = pyflann_ibeis.FLANN()
        nn.build_index(x)

        nnidx, nndist = nn.nn_index(x)
        correct = all(nnidx == np.arange(N, dtype=pyflann_ibeis.index_type))

        nn.delete_index()
        self.assertTrue(correct)

    def testnn_index_random_permute(self):

        numtests = 500
        dim = 10
        N = 100

        nns = [None] * numtests
        x = [rand(N, dim) for i in range(numtests)]
        correct = ones(numtests, dtype=np.bool_)

        for i in np.random.permutation(numtests):
            nns[i] = pyflann_ibeis.FLANN()
            nns[i].build_index(x[i])

            # For kicks
            if rand() < 0.5:
                nns[i].kmeans(x[i], 5)
            if rand() < 0.5:
                nns[i].nn(x[i], x[i])

        for i in np.random.permutation(numtests):
            nnidx, nndist = nns[i].nn_index(x[i])
            correct[i] = all(nnidx == np.arange(N, dtype=pyflann_ibeis.index_type))

        for i in reversed(range(numtests)):
            if rand() < 0.5:
                nns[i].delete_index()
            else:
                del nns[i]

        self.assertTrue(all(correct))

    @pytest.mark.skip('not debugging')
    def testnn_index_bad_index_call_noindex(self):
        nn = pyflann_ibeis.FLANN()
        # self.assertRaises(FLANNException, lambda: nn.nn_index(rand(5, 5)))
        import pytest
        with pytest.raises(pyflann_ibeis.FLANNException):
            nn.nn_index(rand(5, 5))

    @pytest.mark.skip('not debugging')
    def testnn_index_bad_index_call_delindex(self):
        nn = pyflann_ibeis.FLANN()
        nn.build_index(rand(5, 5))
        nn.delete_index()

        with pytest.raises(pyflann_ibeis.FLANNException):
            nn.nn_index(rand(5, 5))
        # self.assertRaises(FLANNException, lambda: nn.nn_index(rand(5, 5)))


if __name__ == '__main__':
    """
    pytest ~/code/flann/tests/test_nn_index.py
    xdoctest ~/code/flann/tests/test_nn_index.py zero
    """
    unittest.main()
