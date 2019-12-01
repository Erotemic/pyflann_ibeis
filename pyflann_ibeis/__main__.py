

def main():  # nocover
    import pyflann_ibeis
    print('Looks like the imports worked')
    print('pyflann_ibeis = {!r}'.format(pyflann_ibeis))
    print('pyflann_ibeis.__file__ = {!r}'.format(pyflann_ibeis.__file__))
    print('pyflann_ibeis.__version__ = {!r}'.format(pyflann_ibeis.__version__))
    print('pyflann_ibeis.flann_ctypes.flannlib = {!r}'.format(pyflann_ibeis.flann_ctypes.flannlib))
    print('pyflann_ibeis.flann_ctypes.libpath = {!r}'.format(pyflann_ibeis.flann_ctypes.libpath))


if __name__ == '__main__':
    """
    CommandLine:
       python -m pyflann_ibeis
    """
    main()
