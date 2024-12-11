import numpy as np
from divtools.model.game_level_2d import GameLevel2D
from typing import List


def horizontal_symmetry(segment: GameLevel2D):
    # # Convert segment to a NumPy array for vectorization
    # if len(segment.map) % 2 == 1:
    #     print(segment.name)
    #     raise ValueError(f"Level's height needs to be an even number")
    # segment = np.array(segment.map)
    #
    # # Calculate the symmetry score using vectorized comparison
    # symmetry = np.sum(segment[:int(len(segment) / 2)] == segment[len(segment) - 1::-1][:int (len(segment) / 2)])

    segment_array = np.array(segment.map)
    height, width = segment_array.shape
    half_height = height // 2
    top_half = segment_array[:half_height]
    bottom_half = segment_array[-half_height:][::-1]

    # Calculate the symmetry score using vectorized comparison
    symmetry = np.sum(top_half == bottom_half)

    return symmetry


def vertical_symmetry(segment):
    # Convert segment to a NumPy array for efficient operations
    segment_array = np.array(segment.map)
    height, width = segment_array.shape

    # Calculate the left and right halves, ignoring the middle column if the width is odd

    half_width = width // 2
    left_half = segment_array[:, :half_width]
    right_half = segment_array[:, -half_width:]

    # Reverse the columns of the right half
    right_half_reversed = right_half[:, ::-1]

    # Calculate the symmetry score using vectorized comparison
    symmetry = np.sum(left_half == right_half_reversed)

    return symmetry


def total_symmetry(segment: GameLevel2D):
    return horizontal_symmetry(segment) + vertical_symmetry(segment)
