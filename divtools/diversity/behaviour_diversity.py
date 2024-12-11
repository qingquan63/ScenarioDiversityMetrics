import numpy as np
from divtools.model.game_level_2d import GameLevel2D


def standard_deviation(levels: list[GameLevel2D], metric: callable, **kwargs) -> float:
    """Calculate the standard deviation of the levels with non-comparison-based metric.

    Parameters:
    ----------
    levels : list[GameLevel2D]
        A list of game levels.

    metric : callable
        A non-comparison-based metric summarizing characteristic of level into a value.

    **kwargs : dict
        Keyword arguments to pass to the metric function.

    Returns:
    -------
    standard_deviation : float
        Return a standard deviation of the levels which is calculated by the metric.

    """
    phi_x = np.array([metric(level, **kwargs) for level in levels])

    return np.std(phi_x)


def _standard_deviation(levels: list[GameLevel2D], metric: callable, **kwargs) -> tuple[np.ndarray, np.ndarray]:
    """Calculate the standard deviation of the levels with non-comparison-based metric.

    Parameters:
    ----------
    levels : list[GameLevel2D]
        A list of game levels.

    metric : callable
        A non-comparison-based metric summarizing characteristic of level into a value.

    Returns:
    -------
    standard_deviation : float
         Return a standard deviation of the levels which is calculated by the metric.

    phi_x : np.ndarray
        Return the metric values of the levels.
    """
    phi_x = np.array([metric(level, **kwargs) for level in levels])

    return np.std(phi_x), phi_x


def behavior_diversity(levels: list[GameLevel2D], metric: callable, p: float = 1, **kwargs) -> float:
    """Calculate the behavior diversity of the levels with non-comparison-based metric.

    Parameters:
    ----------
    levels : list[GameLevel2D]
        A list of game levels.

    metric : callable
        A non-comparison-based metric summarizing characteristic of level into a value.

    p : float ,default = 1
        A weighting parameter for the behavior diversity.

    **kwargs : dict
        Keyword arguments to pass to the metric function.
    Returns:
    -------
    behavior_diversity : float.
        Return the behavior diversity of the levels which is calculated by the standard deviation of the metric.

    """
    N = len(levels)
    delta_phi, phi_x = _standard_deviation(levels, metric, **kwargs)
    phi_max = np.max(phi_x)
    phi_min = np.min(phi_x)
    delta_max = 0.5 * np.sqrt(N / (N - 1)) * (phi_max - phi_min)
    return np.power(delta_phi / delta_max, p)
