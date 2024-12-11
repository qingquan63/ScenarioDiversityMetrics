from divtools.model.game_level_2d import GameLevel2D
import inspect
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt



from divtools.diversity.slacking_a_clipped_function import slacking_a_clipped_function_use_metric


def dissimilarity_map(
        segments_set_x: list[GameLevel2D],
        segments_set_y: list[GameLevel2D],
        metric: callable,
        title_name: str = 'Dissimilarity Map',
        x_label_name: str = 'X Slice Index',
        y_label_name: str = 'Y Slice Index',
        **kwargs
):
    """Draw the dissimilarity map of two sets of game levels.

    Parameters:
    ----------
    segments_set_1 : list[GameLevel2D]
        A list of game levels.
    segments_set_2 : list[GameLevel2D]
        A list of game levels.
    metric : callable
        This function should return metric result for segment.When passing in the metric,
        must pass in the necessary parameters.

    **kwargs : dict
        Additional parameters for the metric function and 'seaborn.heatmap' function.

    """
    # calculate the Euclidean distances/divergence between the original and generated slices
    distances = np.zeros((len(segments_set_y), len(segments_set_x)))
    metric_param = {k: v for k, v in kwargs.items() if k in inspect.signature(metric).parameters}
    for i, segment_y in enumerate(segments_set_y):
        for j, segment_x in enumerate(segments_set_x):
            distances[i, j] = metric(segment_y, segment_x, **metric_param)

    # segment names
    segments_names_y = [segments_set_y[i].name for i in range(len(segments_set_y))]
    segments_names_x = [segments_set_x[i].name for i in range(len(segments_set_x))]

    # Use seaborn.heatmap function to generate heatmaps
    plt.figure(figsize=(10, 8))
    heatmap_param = {k: v for k, v in kwargs.items() if k in inspect.signature(sns.heatmap).parameters}
    if 'annot' not in heatmap_param:
        heatmap_param['annot'] = True
    if 'cmap' not in heatmap_param:
        heatmap_param['cmap'] = 'viridis'
    if 'xticklabels' not in heatmap_param:
        heatmap_param['xticklabels'] = segments_names_x
    if 'yticklabels' not in heatmap_param:
        heatmap_param['yticklabels'] = segments_names_y

    sns.heatmap(distances,**heatmap_param)
    plt.title(title_name)
    plt.xlabel(x_label_name)
    plt.ylabel(y_label_name)

    # # Rotate tick labels for better reading
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

