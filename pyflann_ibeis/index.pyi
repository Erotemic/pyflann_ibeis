import numpy
from numpy import ndarray
from typing import Tuple
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

    def build_index(self, pts, **kwargs):
        ...

    def save_index(self, filename) -> None:
        ...

    def load_index(self, filename, pts) -> None:
        ...

    def used_memory(self):
        ...

    def add_points(self, pts, rebuild_threshold: float = ...) -> None:
        ...

    def remove_point(self, idx) -> None:
        ...

    def nn_index(self, qpts, num_neighbors: int = ..., **kwargs):
        ...

    def nn_radius(self, query, radius, **kwargs):
        ...

    def delete_index(self, **kwargs) -> None:
        ...

    def kmeans(self,
               pts,
               num_clusters,
               max_iterations: Any | None = ...,
               dtype: Any | None = ...,
               **kwargs):
        ...

    def hierarchical_kmeans(self,
                            pts,
                            branch_size,
                            num_branches,
                            max_iterations: Any | None = ...,
                            dtype: Any | None = ...,
                            **kwargs):
        ...

    @property
    def shape(self):
        ...

    @property
    def __len__(self):
        ...

    def get_indexed_shape(self):
        ...

    def get_indexed_data(self):
        ...

    def used_memory_dataset(self):
        ...

    def remove_points(self, idxs) -> None:
        ...
