import numpy as np


def init(p, q, r, t=(-1, -1, -1)):

    def refl(vector, mir):
        return vector - 2 * np.dot(vector, mir) * mir

    def unit(vector):
        magnitude = np.sqrt(np.abs(np.dot(vector, vector)))
        return vector / magnitude

    A, B, C = np.pi / np.array([p, q, r], dtype=np.float64)
    a = - np.cos(A)
    b = + np.sin(A)
    c = - np.cos(B)
    d = (- np.cos(C) - a * c) / b
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
