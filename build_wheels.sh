#!/bin/bash
__doc__="""
SeeAlso:
    ~/code/pyflann_ibeis/pyproject.toml
    ~/code/pyflann_ibeis/dev/docker/make_base_image.py 
"""
# https://cibuildwheel.readthedocs.io/en/stable/options/

#CIBW_BUILD_VERBOSITY=1 \
#CIBW_BEFORE_ALL_LINUX="" \
#CIBW_SKIP='pp*' \
#CIBW_TEST_REQUIRES="-r requirements/tests.txt" \
#CIBW_BUILD="cp37-* cp38-* cp39-* cp310-*" \
#CIBW_TEST_COMMAND='python {project}/run_tests.py' \

#export PIP_GLOBAL_OPTION="-j$(nproc)"
#export PIP_GLOBAL_OPTION="--global-option=-j4"
#export PIP_GLOBAL_OPTION=""

CIBW_ENVIRONMENT="PIP_GLOBAL_OPTION=$PIP_GLOBAL_OPTION" \
CIBW_BEFORE_ALL_LINUX="yum install lz4-devel -y" \
    cibuildwheel --config-file pyproject.toml --platform linux --arch x86_64

#cibuildwheel --config-file pyproject.toml --platform linux --arch x86_64
