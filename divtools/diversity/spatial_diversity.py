import math
from divtools.model.game_level_2d import GameLevel2D


def spatial_diversity(levels: list[GameLevel2D], feature_metric: callable, *args, **kwargs) -> float:
    """
        This function calculates the spatial diversity of a list of game levels.
        It applies a given function to each game level, calculates the entropy of the results,
        and returns a list of these entropy values. It belongs to Non-comparison-based methods.

        Parameters
        ----------
        levels : list[GameLevel2D]
            A list of game levels.
        feature_metric :  callable
            This function should return a float of the metric result for each segment which from the same level.
        *args , **kwargs :
            Additional parameters for the feature_metric function.
        Returns
        -------
        float
            Entropy value for game level.
        """

    res_g = []
    for i in range(len(levels)):
        g_i = feature_metric(levels[i], *args, **kwargs)
        res_g.append(g_i)

    sum_g = sum(res_g)
    entropy = - 1 / math.log(sum_g) * sum(
        [res_g[i] / sum_g * math.log(res_g[i] / sum_g) for i in range(len(res_g)) if res_g[i] > 0])

    return entropy
