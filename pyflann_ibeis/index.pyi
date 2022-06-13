import numpy
from numpy import ndarray
from typing import Tuple
from os import PathLike
from typing import Union
from typing import List
from typing import Any

index_type: Any


def set_distance_type(distance_type, order: int = ...) -> None:
    ...


def to_bytes(string):
    ...


class FLANN:

    def __init__(self, **kwargs) -> None:
        ...

    def __del__(self) -> None:
        ...

    def nn(self,
           pts: numpy.ndarray,
           qpts: numpy.ndarray,
           num_neighbors: int = 1,
           **kwargs) -> Tuple[ndarray, ndarray]:
        ...

    def build_index(self, pts: ndarray, **kwargs):
        ...

    def save_index(self, filename: PathLike) -> None:
        ...

    def load_index(self, filename: PathLike, pts: ndarray) -> None:
        ...

    def used_memory(self) -> int:
        ...

    def add_points(self, pts: ndarray, rebuild_threshold: float = 2.0) -> None:
        ...

    def remove_point(self, idx: int) -> None:
        ...

    def nn_index(self, qpts: ndarray, num_neighbors: int = 1, **kwargs):
        ...

    def nn_radius(self, query: ndarray, radius: float, **kwargs):
        ...

    def delete_index(self, **kwargs) -> None:
        ...

    def kmeans(self,
               pts: numpy.ndarray,
               num_clusters: int,
               max_iterations: Union[int, None] = None,
               dtype: Union[type, None] = None,
               **kwargs):
        ...

    def hierarchical_kmeans(self,
                            pts: numpy.ndarray,
                            branch_size: int,
                            num_branches: int,
                            max_iterations: Union[int, None] = None,
                            dtype: Union[type, None] = None,
                            **kwargs):
        ...

    @property
    def shape(self) -> Tuple:
        ...

    @property
    def __len__(self) -> int:
        ...

    def get_indexed_shape(self) -> Tuple[int, int]:
        ...

    def get_indexed_data(self) -> Tuple[ndarray, ndarray]:
        ...

    def used_memory_dataset(self) -> int:
        ...

    def remove_points(self, idxs: List[int]) -> None:
        ...
