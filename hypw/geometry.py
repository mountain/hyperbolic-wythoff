import numpy as np

from hypw.typing import Transformation, Points, ScalarField, VectorField


def reflect(ps: Points, mir: Transformation) -> Points:
    return ps - 2 * np.sum(ps * mir, axis=-1, keepdims=True) * mir


def radius(ps: Points) -> ScalarField:
    return np.sqrt(np.sum(ps * ps, axis=-1, keepdims=True))


def unify(ps: Points):
    return ps / radius(ps)


def inner(a: VectorField, b: VectorField) -> ScalarField:
    return np.sum(a * b, axis=-1, keepdims=True)


def hbm2pdm(qs: Points) -> Points:  # hyperboloid model to poincare disk model
    return qs[:, :, 1:] / (1 + qs[:, :, 0])


def pdm2hbm(ps: Points) -> Points:  # poincare disk model to hyperboloid model
    rsq = np.sum(ps * ps, axis=2, keepdims=True)
    return np.concatenate([(1 + rsq) * 1j, 2 * ps[:, :, 0:1], 2 * ps[:, :, 1:2]], axis=2) / (1 - rsq)
