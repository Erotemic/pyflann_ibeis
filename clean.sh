#!/bin/bash


rm -rf _skbuild
rm -rf pyflann/lib
rm -rf dist
rm -rf build

CLEAN_PYTHON='find . -regex ".*\(__pycache__\|\.py[co]\)" -delete || find . -iname *.pyc -delete || find . -iname *.pyo -delete'
bash -c "$CLEAN_PYTHON"
