import numpy as np

import hypw.geometry as geom

from hypw.setting import width, linewidth


def checkboard(ps, mirrors):
    u, v, w = mirrors
    rs = np.zeros([width, width, 1], dtype=int)
    ts = np.zeros([width, width, 1], dtype=bool)
    ckb = np.zeros([width, width, 1], dtype=int)
    for count in range(32):
        for m in [u, v, w]:
            pos = geom.inner(ps, m) > 0
            neg = np.logical_not(pos)
            rs = (rs + 1) * neg
            ts = ts | (rs >= 3) & (np.mod(ckb, 2) == 1)
            ps = geom.reflect(ps, m) * pos + ps * neg
            ckb = (ckb + 1) * pos + ckb * neg
    return ts


def edged(ps, mirrors):
    u, v, w = mirrors
    rs = np.zeros([width, width, 1], dtype=int)
    ts = np.zeros([width, width, 1], dtype=bool)
    for count in range(32):
        for m in [u, v, w]:
            pos = geom.inner(ps, m) > 0
            neg = np.logical_not(pos)
            rs = (rs + 1) * neg
            ts = ts | (rs >= 3) & (np.abs(geom.inner(ps, u)) < linewidth)
            ps = geom.reflect(ps, m) * pos + ps * neg
    return ts


def patterned(ps, mirrors, crticplane, pattern):
    u, v, w = mirrors
    rs = np.zeros([width, width, 1], dtype=int)
    ts = np.zeros([width, width, 1], dtype=int)
    for count in range(32):
        for m in [u, v, w]:
            pos = geom.inner(ps, m) > 0
            neg = np.logical_not(pos)
            rs = (rs + 1) * neg
            ts = np.mod(ts + (rs >= 3) * pattern(geom.inner(ps, crticplane)), pattern.base)
            ps = geom.reflect(ps, m) * pos + ps * neg
    return ts



