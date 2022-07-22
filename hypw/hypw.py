import numpy as np
import itertools as it
import hypw.mirror as mir
import hypw.geometry as geom
import hypw.design as dsn
import hypw.color as clr
import hypw.setting as setting
import PIL as pil  # type: ignore

from hypw.typing import Transformation, Order


coord = np.linspace(-1, 1, num=setting.width, dtype=np.complex128)
data = np.array([[x, y] for y in coord for x in coord]).reshape(setting.width, setting.width, 2)


def draw(mirror: Transformation, form, pat):
    disk = geom.radius(data) < 1
    ps = geom.pdm2hbm(data)
    ts = (1 + dsn.patterned(ps, mirror, form, pat)) * disk
    max = np.max(ts)
    crd = len(np.unique(ts))
    return crd, clr.colorbar(max)[ts][:, :, 0, :]


def filename(o: Order, form: int, pat: int):
    p, q, r = o
    a = str(int(p)) if p is not np.inf else 'i'
    b = str(int(q)) if q is not np.inf else 'i'
    c = str(int(r)) if r is not np.inf else 'i'
    return '%s%s%s-%d-%03d.png' % (a, b, c, i, j)


if __name__ == '__main__':
    import time

    start = time.time()

    p, q, r = 2, 3, 7
    mirror = mir.init((p, q, r))
    print(mirror)
    forms = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    for i in range(len(forms)):
        for j in range(128):
            card, img = draw(mirror, forms[i], j)
            if card > 2:
                pil.Image.fromarray(img).save(filename((p, q, r), i, i))

    print("time:", time.time() - start)
