import numpy as np
import numpy.typing as npt


simple = np.array([
    [255, 255, 255, 0],
    [34, 139, 34, 255],
    [188, 143, 143, 255],
], dtype=np.uint8)


accent = np.array([
    [255, 255, 255, 0],
    [ 31, 127, 190, 255],
    [255, 102,   0, 255],
    [ 63, 190, 253, 255],
    [223, 191, 102, 255],
    [ 95, 253, 255, 255],
    [191, 240, 191, 255],
    [127, 255,  56, 255],
    [159,  56, 240, 255],
], dtype=np.uint8)


def colorbar(order: int) -> np.ndarray:
    factor = order // 3 + 1
    incrmt = factor // 3 + 1
    step = 255 // factor
    cmap = [[255, 255, 255, 0]]
    for i in range(order):
        cmap.append([step * (i % factor), step * ((i + incrmt) % factor), step * ((i + 2 * incrmt) % factor), 255])
    return np.array(cmap, dtype=np.uint8)
