#!/bin/bash
__heredoc__="""


notes:

    # TODO: use dind as the base image,
    # Then run the multibuild in docker followed by a test in a different
    # docker container

    # BETTER TODO: 
    # Use a build stage to build in the multilinux environment and then
    # use a test stage with a different image to test and deploy the wheel
    docker run --rm -it --entrypoint="" docker:dind sh
    docker run --rm -it --entrypoint="" docker:latest sh
    docker run --rm -v $PWD:/io -it --entrypoint="" docker:latest sh

    docker run --rm -v $PWD:/io -it python:2.7 bash
     
        cd /io
        pip install -r requirements.txt
        pip install pygments
        pip install wheelhouse/pyflann_ibeis-0.5.0-cp27-cp27mu-manylinux1_x86_64.whl

        cd /
        xdoctest pyflann_ibeis
        pytest io/tests

        cd /io
        python run_tests.py


MB_PYTHON_TAG=cp37-cp37m ./run_multibuild.sh

MB_PYTHON_TAG=cp36-cp36m ./run_multibuild.sh

MB_PYTHON_TAG=cp35-cp35m ./run_multibuild.sh

MB_PYTHON_TAG=cp27-cp27m ./run_multibuild.sh

# MB_PYTHON_TAG=cp27-cp27mu ./run_nmultibuild.sh

"""


get_native_mb_python_tag(){
    __heredoc__='''
    Get the MB tag for the current version of python running
    
    https://stackoverflow.com/questions/53409511/what-is-the-difference-between-cpython-27m-and-27mu?noredirect=1&lq=1
    '''
    # TODO: get if cp27m or cp27mu
    python -c "
import sys
import platform
major = sys.version_info[0]
minor = sys.version_info[1]
ver = '{}{}'.format(major, minor)
if platform.python_implementation() == 'CPython':
    impl = 'cp'
    abi = 'm'
else:
    raise NotImplementedError(impl)
mb_tag = '{impl}{ver}-{impl}{ver}{abi}'.format(**locals())
print(mb_tag)
"
}


#DOCKER_IMAGE=${DOCKER_IMAGE:="soumith/manylinux-cuda100"}
DOCKER_IMAGE=${DOCKER_IMAGE:="quay.io/pypa/manylinux2010_x86_64"}
#PARENT_USER=${PARENT_USER:="$USER"}

# Valid multibuild python versions are:
# cp27-cp27m  cp27-cp27mu  cp34-cp34m  cp35-cp35m  cp36-cp36m  cp37-cp37m
MB_PYTHON_TAG=${MB_PYTHON_TAG:=$(get_native_mb_python_tag)}


if [ "$_INSIDE_DOCKER" != "YES" ]; then

    set -e
    docker run --rm \
        -v $PWD:/io \
        -e _INSIDE_DOCKER="YES" \
        -e MB_PYTHON_TAG="$MB_PYTHON_TAG" \
        $DOCKER_IMAGE bash -c 'cd /io && ./run_multibuild.sh'

    __interactive__='''
    docker run --rm \
        -v $PWD:/io \
        -e _INSIDE_DOCKER="YES" \
        -e MB_PYTHON_TAG="$MB_PYTHON_TAG" \
        -it $DOCKER_IMAGE bash

    set +e
    set +x
    '''

    exit 0;
fi


set -x
set -e

yum install lz4-devel -y


# Define multibuild workdir where we will try to store all temporary files
MB_WORKDIR=mb_work
mkdir -p $MB_WORKDIR
chmod -R o+rw $MB_WORKDIR


PYPREFIX=/opt/python/$MB_PYTHON_TAG
PYEXE=${PYPREFIX}/bin/python
VENV_DIR=$MB_WORKDIR/venv_$MB_PYTHON_TAG

echo "VENV_DIR = $VENV_DIR"

$PYEXE --version  # Print out python version for debugging
$PYEXE -m pip install virtualenv
$PYEXE -m virtualenv $VENV_DIR

chmod -R o+rw $VENV_DIR
#setfacl -d -m g::rwx $VENV_DIR
#setfacl -d -m o::rwx $VENV_DIR

set +x
echo "activate virtualenv"
source $VENV_DIR/bin/activate
echo "activated virtualenv"
set -x

export PIP_CACHE_DIR="$MB_WORKDIR/cache_pip"

pip install pip -U
pip install pip setuptools -U

#pip install -r requirements.txt
# we only need build requirements to make the wheel
pip install -r requirements/build.txt

chmod -R o+rw $VENV_DIR

python setup.py bdist_wheel

chmod -R o+rw _skbuild
chmod -R o+rw dist

auditwheel repair dist/pyflann_ibeis-*-$MB_PYTHON_TAG-*.whl
chmod -R o+rw wheelhouse

chmod -R o+rw pyflann_ibeis.egg-info
