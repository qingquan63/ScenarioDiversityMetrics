from typing import List, Set, Tuple
from divtools.model.game_level_2d import GameLevel2D


def get_similar_rows(training_data: List[GameLevel2D]):
    similar_rows = set()
    for train_segment in training_data:
        for row in train_segment.map:
            similar_rows.add(tuple(row))
    return similar_rows


def get_similar_cols(training_data: List[GameLevel2D]):
    similar_cols = set()
    for train_segment in training_data:
        map = [list(row) for row in zip(*train_segment.map)]
        for row in map:
            similar_cols.add(tuple(row))
    return similar_cols


def similarity(segment: GameLevel2D, similar_rows: Set[Tuple], similar_cols: Set[Tuple]):
    res = 0
    for row in segment.map:
        # Convert the row to a tuple for consistency
        row_tuple = tuple(row)
        # Check if the row appears in the preprocessed training data
        if row_tuple in similar_rows:
            res += 1

    map_t = [list(row) for row in zip(*segment.map)]

    for col in map_t:
        col_tuple = tuple(col)

        if col_tuple in similar_cols:
            res += 1
    return res
