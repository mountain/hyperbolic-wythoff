import numpy as np

import hypw.geometry as geom
import hypw.mirror as mir

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
    #u, v, w = mirrors
    #rs = np.zeros([width, width, 1], dtype=int)
    #ts = np.zeros([width, width, 1], dtype=bool)
    #for count in range(32):
    #    for m in [u, v, w]:
    #        pos = geom.inner(ps, m) > 0
    #        neg = np.logical_not(pos)
    #        rs = (rs + 1) * neg
    #        ts = ts | (rs >= 3) & (np.abs(geom.inner(ps, u)) < linewidth)
    #        ps = geom.reflect(ps, m) * pos + ps * neg
    #return ts
    return patterned(ps, mirrors, (1, 0, 1), 16)


def patterned(ps, mirrors, form, pat):
    u, v, w = mirrors
    a, b, c = mir.critical_plane(mirrors, form)

    rs = np.zeros([width, width, 1], dtype=int)
    ts = np.zeros([width, width, 1], dtype=bool)
    flag = np.array([(pat >> n) & 1 for n in range(6)], dtype=np.bool)
    coef = np.power(2, np.cumsum(flag)) * flag
    for count in range(32):
        for m in [u, v, w]:
            pos = geom.inner(ps, m) > 0
            neg = np.logical_not(pos)
            blka = geom.inner(ps, a) > 0
            blkb = geom.inner(ps, b) < 0
            blkc = geom.inner(ps, c) > 0
            code = coef[0] * blka + coef[1] * blkb + coef[2] * blkc

            edgu = np.abs(geom.inner(ps, u)) < linewidth
            edgv = np.abs(geom.inner(ps, v)) < linewidth
            edgw = np.abs(geom.inner(ps, w)) < linewidth
            code = code + coef[3] * edgu + coef[4] * edgv + coef[5] * edgw

            rs = (rs + 1) * neg
            ts = ts | (rs >= 3) * code
            ps = geom.reflect(ps, m) * pos + ps * neg
    return ts



