#!/usr/bin/env bash
__doc__="
Runs cibuildwheel to create linux binary wheels.

Requirements:
    pip install cibuildwheel

SeeAlso:
    pyproject.toml
"

if ! which docker ; then
    echo "Missing requirement: docker. Please install docker before running build_wheels.sh"
    exit 1
fi
if ! which cibuildwheel ; then
    echo "The cibuildwheel module is not installed. Please pip install cibuildwheel before running build_wheels.sh"
    exit 1
fi


#pip wheel -w wheelhouse .
# python -m build --wheel -o wheelhouse  #  pyflann_ibeis: +COMMENT_IF(binpy)
cibuildwheel --config-file pyproject.toml --platform linux --archs x86_64  #  pyflann_ibeis: +UNCOMMENT_IF(binpy)

export CIBW_CONFIG_SETTINGS: --build-option=--py-limited-api=cp38
cibuildwheel --config-file pyproject.toml --platform linux --archs x86_64  #  pyflann_ibeis: +UNCOMMENT_IF(binpy)
