|GithubActions| |ReadTheDocs| |Pypi| |Downloads| |Codecov| 


This is a Fork of the FLANN repo, under a different name for use in the IBEIS
project. The main difference is that it has a few more helper function calls
and it should be easier build wheels and to pip install.


FLANN - Fast Library for Approximate Nearest Neighbors
======================================================

FLANN is a library for performing fast approximate nearest neighbor searches in high dimensional spaces. It contains a collection of algorithms we found to work best for nearest neighbor search and a system for automatically choosing the best algorithm and optimum parameters depending on the dataset.
FLANN is written in C++ and contains bindings for the following languages: C, MATLAB, Python, and Ruby.


Documentation
-------------

Check FLANN web page [here](http://www.cs.ubc.ca/research/flann).

Documentation on how to use the library can be found in the doc/manual.pdf file included in the release archives.

More information and experimental results can be found in the following paper:

  * Marius Muja and David G. Lowe, "Fast Approximate Nearest Neighbors with Automatic Algorithm Configuration", in International Conference on Computer Vision Theory and Applications (VISAPP'09), 2009 [(PDF)](http://people.cs.ubc.ca/~mariusm/uploads/FLANN/flann_visapp09.pdf) [(BibTex)](http://people.cs.ubc.ca/~mariusm/index.php/FLANN/BibTex)


Getting FLANN
-------------

If you want to try out the latest changes or contribute to FLANN, then it's recommended that you checkout the git source repository: `git clone git://github.com/mariusmuja/flann.git`

If you just want to browse the repository, you can do so by going [here](https://github.com/mariusmuja/flann).


Conditions of use
-----------------

FLANN is distributed under the terms of the [BSD License](https://github.com/mariusmuja/flann/blob/master/COPYING).

Bug reporting
-------------

Please report bugs or feature requests using [github's issue tracker](http://github.com/mariusmuja/flann/issues).


.. |CircleCI| image:: https://circleci.com/gh/Erotemic/pyflann_ibeis.svg?style=svg
    :target: https://circleci.com/gh/Erotemic/pyflann_ibeis
.. |Travis| image:: https://img.shields.io/travis/Erotemic/pyflann_ibeis/main.svg?label=Travis%20CI
   :target: https://travis-ci.org/Erotemic/pyflann_ibeis?branch=main
.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Erotemic/pyflann_ibeis?branch=main&svg=True
   :target: https://ci.appveyor.com/project/Erotemic/pyflann_ibeis/branch/main
.. |Codecov| image:: https://codecov.io/github/Erotemic/pyflann_ibeis/badge.svg?branch=main&service=github
   :target: https://codecov.io/github/Erotemic/pyflann_ibeis?branch=main
.. |Pypi| image:: https://img.shields.io/pypi/v/pyflann_ibeis.svg
   :target: https://pypi.python.org/pypi/pyflann_ibeis
.. |Downloads| image:: https://img.shields.io/pypi/dm/pyflann_ibeis.svg
   :target: https://pypistats.org/packages/pyflann_ibeis
.. |ReadTheDocs| image:: https://readthedocs.org/projects/pyflann_ibeis/badge/?version=latest
    :target: http://pyflann_ibeis.readthedocs.io/en/latest/
.. |GithubActions| image:: https://github.com/Erotemic/pyflann_ibeis/actions/workflows/test_binaries.yml/badge.svg?branch=main
    :target: https://github.com/Erotemic/pyflann_ibeis/actions?query=branch%3Amain
