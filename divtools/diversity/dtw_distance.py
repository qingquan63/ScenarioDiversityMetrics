from dtw import *
import numpy as np
from divtools.model.game_trace_2d import GameTraceWithTime
from divtools.model.game_trace_2d import Position2D


def dtw_distance_with_time(trace1: GameTraceWithTime, trace2: GameTraceWithTime) -> float:
    """
        This function calculates the Dynamic Time Warping (DTW) distance between two game traces.
        It uses the DTW algorithm to find the optimal alignment between two sequences of game positions.

        Parameters:
        trace1 (GameTraceWithTime): The first game trace.
        trace2 (GameTraceWithTime): The second game trace.

        Returns:
        float: The DTW distance between the two game traces.
        """
    n = len(trace1.positions)
    m = len(trace2.positions)
    # get the positions of the traces
    trace1_positions = np.array([[pos.x, pos.y] for _, pos in trace1.positions])
    trace2_positions = np.array([[pos.x, pos.y] for _, pos in trace2.positions])

    # keep_internals=True remains the internal matrices of the DTW algorithm
    # distance_only=True only returns the DTW distance
    # step_pattern adjusts the step pattern of the DTW algorithm
    alignment = dtw(trace1_positions, trace2_positions, keep_internals=True, distance_only=False,
                    step_pattern="symmetric1")
    print(alignment.index1, alignment.index2)
    print(alignment.index1s, alignment.index2s)
    # alignment.plot(type="twoway")
    return alignment.distance

if __name__ == '__main__':

    positions_with_time = [
        (1.0, [10, 20]),
        (2.0, [20, 30]),
        (3.5, [40, 50])
    ]

    a = GameTraceWithTime(position_type=Position2D, positions=positions_with_time)
    b = GameTraceWithTime(position_type=Position2D, positions=positions_with_time)
    print(dtw_distance_with_time(a, b))