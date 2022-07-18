import numpy as np
from numpy.typing import NDArray
from typing import TypeVar, Generic, Tuple, Union, Optional

Order = Tuple[int, int, int]
Point = Tuple[float, float, float]

Transformation = NDArray[np.complex128]
Points = NDArray[np.complex128]

ScalarField = NDArray[np.complex128]
VectorField = NDArray[np.complex128]
