import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from divtools.model.game_level_2d import GameLevel2D


def is_pareto_efficient(costs):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            # Keep any point with a higher cost
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)
            is_efficient[i] = True  # And keep self
    return is_efficient


def draw_pareto_front_3d(metric_score, metric_x: str, metric_y: str, metric_z: str, **kwargs):
    pareto_mask = is_pareto_efficient(metric_score)
    pareto_front = metric_score[pareto_mask]
    non_pareto_front = metric_score[~pareto_mask]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(non_pareto_front[:, 0], non_pareto_front[:, 1], non_pareto_front[:, 2], label='Scenario')
    ax.scatter(pareto_front[:, 0], pareto_front[:, 1], pareto_front[:, 2], color='red', label='Pareto Front')
    ax.set_xlabel(metric_x)
    ax.set_ylabel(metric_y)
    ax.set_zlabel(metric_z)
    ax.set_title('Pareto Front Visualization')
    ax.legend()
    plt.show()
