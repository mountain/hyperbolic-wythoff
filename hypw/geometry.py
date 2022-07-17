import numpy as np


def reflect(ps, mir):
    return ps - 2 * np.sum(ps * mir, axis=-1, keepdims=True) * mir


def radius(ps):
    return np.sqrt(np.sum(ps * ps, axis=-1, keepdims=True))


def unify(ps):
    return ps / radius(ps)


def inner(a, b):
    return np.sum(a * b, axis=-1, keepdims=True)


def hbm2pdm(qs):  # hyperboloid model to poincare disk model
    return qs[:, :, 1:] / (1 + qs[:, :, 0])


def pdm2hbm(ps):  # poincare disk model to hyperboloid model
    rsq = np.sum(ps * ps, axis=2, keepdims=True)
    return np.concatenate([(1 + rsq) * 1j, 2 * ps[:, :, 0:1], 2 * ps[:, :, 1:2]], axis=2) / (1 - rsq)
