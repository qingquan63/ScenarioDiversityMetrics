import numpy as np
import itertools
import zlib
import gzip
from divtools.model.game_level_2d import GameLevel2D

def compress(data):
    """使用zlib、gzip压缩数据."""
    return gzip.compress(data)


def ncd(level1: GameLevel2D, level2: GameLevel2D):
    l1_flatten = list(itertools.chain.from_iterable(level1.map))
    l2_flatten = list(itertools.chain.from_iterable(level2.map))
    l1 = np.asarray(l1_flatten)
    l2 = np.asarray(l2_flatten)

    serialize1 = l1.tobytes()
    serialize2 = l2.tobytes()

    c_x = len(compress(serialize1))
    c_y = len(compress(serialize2))
    c_xy = len(compress(serialize1 + serialize2))

    return (c_xy - min(c_x, c_y)) / max(c_x, c_y)

