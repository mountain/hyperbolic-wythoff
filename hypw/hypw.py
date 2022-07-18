import numpy as np
import hypw.mirror as mir
import hypw.geometry as geom
import hypw.design as dsn
import hypw.color as clr
import hypw.setting as setting
import PIL as pil  # type: ignore

from hypw.typing import Transformation, Order, Point


coord = np.linspace(-1, 1, num=setting.width, dtype=np.complex128)
data = np.array([[x, y] for y in coord for x in coord]).reshape(setting.width, setting.width, 2)


def draw(mirror: Transformation):
    disk = geom.radius(data) < 1
    ps = geom.pdm2hbm(data)
    ts = dsn.checkboard(ps, mirror)
    return clr.colormap[(2 * disk - ts) * disk][:, :, 0, :]


def filename(o: Order):
    p, q, r = o
    a = str(int(p)) if p is not np.inf else 'i'
    b = str(int(q)) if q is not np.inf else 'i'
    c = str(int(r)) if r is not np.inf else 'i'
    return '%s%s%s.png' % (a, b, c)


if __name__ == '__main__':
    import time

    start = time.time()

    p, q, r = 3, 3, 4
    mirror = mir.init(p, q, r)
    print(mirror)
    img = pil.Image.fromarray(draw(mirror))
    img.save(filename(p, q, r))

    print("time:", time.time() - start)
