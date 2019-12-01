#!/bin/bash
__heredoc__="""
sudo apt-get install libhdf5-serial-dev
sudo apt install liblz4-dev
"""

python setup.py build_ext --inplace
python setup.py develop
