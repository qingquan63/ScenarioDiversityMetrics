from divtools.model.game_level_2d import GameLevel2D


def gini_simpson_index(levels: list[GameLevel2D], metric: callable, **kwargs) -> float:
    """
    Calculate the Gini-Simpson index of a given dataset. It belongs to Non-comparison-based methods.

    Parameters
    ----------
    levels : list[GameLevel2D]
        A list of game levels.
    metric : callable
        This function should return a metric result for each segment.
    Returns
    -------
    float
        The Gini-Simpson index.

    Examples
    --------

    """
    phi = []
    sum_phi = 0
    for lvl in levels:
        metric_result = metric(lvl, **kwargs)
        phi.append(metric_result)
        sum_phi += metric_result
    for i in range(len(phi)):
        phi[i] = (phi[i] / sum_phi) ** 2

    return 1 - sum(phi)
