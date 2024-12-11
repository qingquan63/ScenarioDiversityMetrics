from divtools.model.game_level_2d import GameLevel2D


def density_metric(segment: GameLevel2D, block_char, mapping: dict = None) -> int:
    """
    Calculate the density of a given segment.

    Parameters
    ----------
    segment : GameLevel2D
        A game level.
    block_char : str or int
        The block character.
    mapping : dict
        A dictionary that maps block characters to integers.
    Returns
    -------
    int
        The density of the segment.

    Examples
    --------
    """
    block_index = 0
    if isinstance(block_char, str):
        if mapping is None:
            raise ValueError("mapping must be provided when block_char is a string")
        block_index = mapping[block_char]
    elif isinstance(block_char, int):
        block_index = block_char
    else:
        raise ValueError("block_char must be a string or an integer")
    count_of_block = sum(sub.count(block_index) for sub in segment.map)
    sum_elements = sum(len(sub) for sub in segment.map)

    return sum_elements - count_of_block
