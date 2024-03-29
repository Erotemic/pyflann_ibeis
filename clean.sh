#!/bin/bash


rm -rf _skbuild
rm -rf pyflann/lib
rm -rf dist
rm -rf build
rm -rf htmlcov
rm -rf pyflann_ibeis.egg-info

rm -rf mb_work
rm -rf wheelhouse
rm -rf pyflann_ibeis/lib/lib*

CLEAN_PYTHON='find . -regex ".*\(__pycache__\|\.py[co]\)" -delete || find . -iname *.pyc -delete || find . -iname *.pyo -delete'
bash -c "$CLEAN_PYTHON"
