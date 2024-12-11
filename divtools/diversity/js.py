import copy

from kl import *


def js_divergence(p, q):
    """
    Compute the Jensen-Shannon divergence between two probability distributions.
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)


def js_divergence_2d(level1: GameLevel2D, level2: GameLevel2D, eye=2):
    """
    Compute the Jensen-Shannon divergence between two 2D game levels.
    """

    if eye not in level1.tile_pattern:
        level1_prob = level1.tile_pattern[eye] = find_pattern(level1, eye)
    else:
        level1_prob = level1.tile_pattern[eye]

    if eye not in level2.tile_pattern:
        level2_prob = level2.tile_pattern[eye] = find_pattern(level2, eye)
    else:
        level2_prob = level2.tile_pattern[eye]
    # level1_prob = find_pattern(level1, eye)
    middle_prob = copy.deepcopy(level1_prob)
    # level2_prob = find_pattern(level2, eye)
    middle_prob.update(level2_prob)

    # 对每个元素的计数除以2
    total_middle = sum(middle_prob.values())
    for key in middle_prob:
        middle_prob[key] /= total_middle

    pattern_key_1 = set(level1_prob.keys())
    pattern_key_2 = set(level2_prob.keys())
    # 0.5 * KL(P||M) + 0.5 * KL(Q||M)
    values_1 = [level1_prob[key] for key in pattern_key_1]
    values_1 = get_prob(values_1)

    values_middle_1 = [middle_prob[key] for key in pattern_key_1]

    values_2 = [level2_prob[key] for key in pattern_key_2]

    values_2 = get_prob(values_2)

    values_middle_2 = [middle_prob[key] for key in pattern_key_2]

    return 0.5 * kl_divergence(values_1, values_middle_1) + 0.5 * kl_divergence(values_2, values_middle_2)
