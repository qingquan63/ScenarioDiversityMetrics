import numpy as np
import inspect
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from divtools.model.game_level_2d import GameLevel2D


def tsne_visualization(
        levels: list[GameLevel2D],
        title_name: str = 't-SNE Visualization of the Levels',
        x_label_name: str = 'Dimension 1',
        y_label_name: str = 'Dimension 2',
        **kwargs
) -> None:
    """This function visualizes the t-SNE of the game levels.

    Parameters:
    ----------
    levels : list[GameLevel2D]
        A list of game levels.
    **kwargs : dict
        Additional parameters for the 't-SNE' and 'matplotlib.plt.figure' function.

    Returns:
    -------
    None

    """
    tsne_visualization.__name__ = 't-Sne Visualization'
    plt_figure_param = {k: v for k, v in kwargs.items() if k in inspect.signature(plt.figure).parameters}
    tsne_param = {k: v for k, v in kwargs.items() if k in inspect.signature(TSNE).parameters}

    if 'n_components' not in tsne_param:
        tsne_param['n_components'] = 2
    if 'init' not in tsne_param:
        tsne_param['init'] = 'pca'
    if 'perplexity' not in tsne_param:
        tsne_param['perplexity'] = min(len(levels) - 1, 30)

    transformed_data = None
    if tsne_param['metric'] == 'precomputed':
        tsne_param['init'] = 'random'
        distance_matrix = kwargs['distance_matrix']
        tsne = TSNE(**tsne_param)
        transformed_data = tsne.fit_transform(distance_matrix)
    else:
        data = [level.map for level in levels]
        data = np.array(data)
        data_flattened = data.reshape(len(levels), -1)
        tsne = TSNE(**tsne_param)
        transformed_data = tsne.fit_transform(data_flattened)

    labels = [level.label for level in levels]

    labels = np.array(labels)

    plt.figure(**plt_figure_param)
    # Remove duplicates from the labels
    unique_labels = set(labels)
    # Sort the labels
    unique_labels = list(unique_labels)
    unique_labels = sorted(unique_labels)
    for label in unique_labels:
        mask = labels == label
        plt.scatter(transformed_data[mask, 0], transformed_data[mask, 1], label=f' {label}', alpha=0.5)

    plt.grid(False)
    plt.legend()
    plt.title(title_name)
    plt.xlabel(x_label_name)
    plt.ylabel(y_label_name)
    plt.show()

