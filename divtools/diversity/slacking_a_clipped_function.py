from divtools.model.game_level_2d import GameLevel2D


def a_clip_function(d_x, g, r) -> float:
    return min(r, 1 - abs(d_x - g) / g)


def _r_k(k, n):
    return 1 - k / (n + 1)


def slacking_a_clipped_function(metric_resulting_matrix: list[list], g: float = 0.1,
                                max_memory_capacity: int = 4) -> list:
    """The purpose of this function is to calculate the fun of each level segment in a given game level design.It is
    achieved by adjusting the difference between each level segment and the first n levels.

    Parameters
    ----------
    metric_resulting_matrix : list[list]
        2D list of metric results between segments pairwise.

    g : float , default = 0.1
        Parameter that is set for metric.

    max_memory_capacity : int , default = 4
        The maximum number of previous segments that could be memorised by a player.

    Returns
    -------
    fun_degree : float
        A list of the degree of fun of each level segment.
    """
    fx = []
    for i in range(len(metric_resulting_matrix)):
        up_bound = min(i+1, max_memory_capacity)
        sum_of_ac = sum(a_clip_function(metric_resulting_matrix[i][i - k], g, _r_k(k, max_memory_capacity)) for k in range(up_bound))
        r = sum(_r_k(k, max_memory_capacity) for k in range(up_bound))
        fx.append(sum_of_ac / r)

    return fx


def slacking_a_clipped_function_use_metric(levels: list[GameLevel2D], metric: callable, g: float = 0.1,
                                           max_memory_capacity: int = 4, **kwargs) -> list:
    """The purpose of this function is to calculate the fun of each level segment in a given game level design.It is
    achieved by adjusting the difference between each level segment and the first n levels.

    Parameters
    ----------

    levels : list[GameLevel2D]
        A list of game levels.

    metric : callable
        This function should return metric result for segment.When passing in the metric,
        must pass in the necessary parameters in kwargs.

    g : float , default = 0.1
        Parameter that is set for metric.

    max_memory_capacity : int , default = 4
        The maximum number of previous segments that could be memorised by a player.

    **kwargs : dict
        Additional parameters for the metric function.
    """
    metric_resulting_matrix = [[metric(level_i, level_j, **kwargs) for level_j in levels] for level_i in levels]
    return slacking_a_clipped_function(metric_resulting_matrix, g, max_memory_capacity)
