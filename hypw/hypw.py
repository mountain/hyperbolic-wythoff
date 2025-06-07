import numpy as np
import itertools as it
import hypw.mirror as mir
import hypw.geometry as geom
import hypw.design as dsn
import hypw.color as clr
import hypw.setting as setting
import PIL as pil  # type: ignore
import argparse

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
    return '%s%s%s-%d-%03d.png' % (a, b, c, form, pat)


if __name__ == '__main__':
    import time

    parser = argparse.ArgumentParser(description="Generate hyperbolic tilings.")
    parser.add_argument('--p', type=int, default=2, help='Parameter p for the Schwarz triangle (default: 2)')
    parser.add_argument('--q', type=int, default=3, help='Parameter q for the Schwarz triangle (default: 3)')
    parser.add_argument('--r', type=int, default=7, help='Parameter r for the Schwarz triangle (default: 7)')
    args = parser.parse_args()

    start = time.time()

    p, q, r = args.p, args.q, args.r
    mirror = mir.init((p, q, r))
    print(mirror)
    # Each tuple in 'forms' likely represents a specific configuration for the tiling pattern.
    # These could be defined as named constants if their specific meanings are known,
    # e.g., FORM_A = (0, 0, 1), FORM_B = (0, 1, 0), etc.
    forms = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    for i in range(len(forms)):
        # Iterate through a set of 128 pattern variations
        for j in range(128):
            card, img = draw(mirror, forms[i], j)
            # Save the image only if it has a minimum level of complexity (more than 2 distinct regions/colors)
            if card > 2:
                pil.Image.fromarray(img).save(filename((p, q, r), i, i))

    print("time:", time.time() - start)
