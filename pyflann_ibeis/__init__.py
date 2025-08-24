#Copyright 2008-2009  Marius Muja (mariusm@cs.ubc.ca). All rights reserved.
#Copyright 2008-2009  David G. Lowe (lowe@cs.ubc.ca). All rights reserved.
#
#THE BSD LICENSE
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions
#are met:
#
#1. Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__version__ = '2.4.1'
__author__ = 'Marius Muja, David G. Lowe, Jon Crall'
__author_email__ = 'erotemic@gmail.com'
__url__ = 'https://github.com/Erotemic/pyflann_ibeis'

__autogen__ = """
mkinit pyflann_ibeis
"""


from pyflann_ibeis import exceptions
from pyflann_ibeis import flann_ctypes
from pyflann_ibeis import index

from pyflann_ibeis.exceptions import (FLANNException,)
from pyflann_ibeis.flann_ctypes import (CustomStructure, FLANNParameters,
                                        FLANN_INDEX, FlannLib, STRING,
                                        allowed_types, default_flags,
                                        define_functions, ensure_2d_array,
                                        flann, flannlib, load_flann_library,
                                        type_mappings,)
from pyflann_ibeis.index import (FLANN, index_type, set_distance_type,
                                 to_bytes,)

__all__ = ['CustomStructure', 'FLANN', 'FLANNException', 'FLANNParameters',
           'FLANN_INDEX', 'FlannLib', 'STRING', 'allowed_types',
           'default_flags', 'define_functions', 'ensure_2d_array',
           'exceptions', 'flann', 'flann_ctypes', 'flannlib', 'index',
           'index_type', 'load_flann_library', 'set_distance_type', 'to_bytes',
           'type_mappings']
