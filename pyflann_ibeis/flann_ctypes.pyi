from numpy import ndarray
from ctypes import Structure, c_char_p, c_void_p
from typing import Any, Callable, Dict

STRING = c_char_p


class CustomStructure(Structure):

    def __init__(self) -> None:
        ...

    def update(self, dict) -> None:
        ...

    def __getitem__(self, k):
        ...

    def __setitem__(self, k, v) -> None:
        ...

    def keys(self):
        ...


class FLANNParameters(CustomStructure):
    ...


default_flags: Any
allowed_types: Any
FLANN_INDEX = c_void_p


def load_flann_library():
    ...


flannlib: Any
libpath: Any


class FlannLib:
    build_index: Dict[Any, Callable]
    save_index: Dict[Any, Callable]
    load_index: Dict[Any, Callable]
    used_memory: Dict[Any, Callable]
    add_points: Dict[Any, Callable]
    remove_point: Dict[Any, Callable]
    find_nearest_neighbors: Dict[Any, Callable]
    find_nearest_neighbors_index: Dict[Any, Callable]
    radius_search: Dict[Any, Callable]
    compute_cluster_centers: Dict[Any, Callable]


flann: Any
type_mappings: Any


def define_functions(text: str):
    ...


def ensure_2d_array(arr: ndarray, flags: Any, **kwargs):
    ...
