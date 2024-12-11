import copy
import numpy as np
from collections import Counter
from divtools.model.game_level_2d import GameLevel2D


def kl_divergence(p, q):
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    q = np.where(q != 0, q, np.finfo(float).eps)

    return np.sum(np.where(p != 0, p * np.log2(p / q), 0))


def find_pattern(level: GameLevel2D, eye):
    patterns = Counter()
    lvl_list = level.map
    level_map = np.array(lvl_list)

    if level_map.shape[0] < eye or level_map.shape[1] < eye:
        return patterns

    for i in range(level_map.shape[0] - (eye - 1)):
        for j in range(level_map.shape[1] - (eye - 1)):
            # Extract the 2x2 sub-array
            sub_array = level_map[i:i + eye, j:j + eye]
            # Convert the sub-array to a tuple and count it
            patterns[tuple(map(tuple, sub_array))] += 1

    return patterns


def kl_divergence_2d(level1: GameLevel2D, level2: GameLevel2D, eye=2):
    patterns_original = find_pattern(level1, eye)
    patterns_copy = copy.deepcopy(patterns_original)
    patterns_copy = find_level_pattern(patterns_copy, level2.map, eye)

    pattern_key = set(patterns_original.keys())
    values1 = [patterns_original[key] for key in pattern_key]
    values2 = [patterns_copy[key] for key in pattern_key]

    return kl_divergence(values1, values2)


def find_level_pattern(patterns: Counter, level2: list, eye):
    for p in patterns:
        patterns[p] = 0
    level2_map = np.asarray(level2)
    for i in range(level2_map.shape[0] - (eye - 1)):
        for j in range(level2_map.shape[1] - (eye - 1)):
            # Extract the 2x2 sub-array
            sub_array = level2_map[i:i + eye, j:j + eye]
            if tuple(map(tuple, sub_array)) in patterns:
                patterns[tuple(map(tuple, sub_array))] += 1
    return patterns


def get_prob(x: list[int]):
    total = sum(x)
    return [i / total for i in x]
