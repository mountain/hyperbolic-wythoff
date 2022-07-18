import numpy as np

from hypw.typing import Order, Point, Transformation, Planes


def init(o: Order, t: Point = (-1, -1, -1)) -> Transformation:
    def refl(vector, mir):
        return vector - 2 * np.dot(vector, mir) * mir

    def unit(vector):
        magnitude = np.sqrt(np.abs(np.dot(vector, vector)))
        return vector / magnitude

    alpha, beta, gamma = np.pi / np.array(o, dtype=np.float64)
    a = - np.cos(alpha)
    b = + np.sin(alpha)
    c = - np.cos(beta)
    d = (- np.cos(gamma) - a * c) / b
    e = 1j * np.sqrt(np.abs(1 - c * c - d * d))
    mirrors = np.array([
        [0, 1, 0],
        [0, a, b],
        [e, c, d]
    ], dtype=np.complex128)

    omni = unit(np.linalg.solve(mirrors, np.array(t)))
    if omni[0].imag < 0:
        omni = - omni
    temp = unit(omni - np.array([1j, 0, 0]))

    for j, m in enumerate(mirrors):
        target = refl(m, temp)
        if target[0].imag < 0:
            target = - target
        mirrors[j] = target

    return mirrors


def critical_plane(mirrors: Transformation, t: Point = (0, 1, 1)) -> Transformation:
    u, v, w = mirrors
    vertex = np.linalg.solve(mirrors, np.array(t))
    return 1j * np.cross(vertex, v)
