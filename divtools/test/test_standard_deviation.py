import unittest
from symmetry import total_symmetry
from divtools.diversity.behaviour_diversity import standard_deviation, behavior_diversity
from divtools.model.game_level_2d import GameLevel2D
import time


class MyTestCase(unittest.TestCase):
    def test_standard_deviation(self):
        levels = [GameLevel2D([[1, 2, 3, 4], [2, 3, 4, 4], [2, 3, 4, 4], [2, 3, 4, 4]], "level1"),
                  GameLevel2D([[2, 3, 4, 4], [3, 4, 5, 4], [2, 3, 4, 4], [2, 3, 4, 4]], "level1"),
                  GameLevel2D([[3, 4, 5, 5], [4, 5, 6, 5], [2, 3, 4, 5], [2, 3, 4, 4]], "level2"),
                  GameLevel2D([[4, 5, 6, 5], [5, 6, 7, 5], [2, 3, 4, 5], [2, 3, 4, 4]], "level2"),
                  GameLevel2D([[5, 6, 7, 6], [6, 7, 8, 6], [2, 3, 4, 6], [2, 3, 4, 4]], "level3"),
                  GameLevel2D([[3, 2, 1, 6], [6, 7, 8, 6], [2, 3, 4, 6], [2, 3, 4, 4]], "level4"),
                  GameLevel2D([[9, 2, 7, 3], [6, 7, 8, 3], [2, 3, 4, 3], [2, 3, 4, 4]], "level5")]
        a = standard_deviation(levels, total_symmetry)

    def test_behavior_diversity(self):
        levels = [GameLevel2D([[1, 2, 3, 4], [2, 3, 4, 4], [2, 3, 4, 4], [2, 3, 4, 4]], "level1"),
                  GameLevel2D([[2, 3, 4, 4], [3, 4, 5, 4], [2, 3, 4, 4], [2, 3, 4, 4]], "level1"),
                  GameLevel2D([[3, 4, 5, 5], [4, 5, 6, 5], [2, 3, 4, 5], [2, 3, 4, 4]], "level2"),
                  GameLevel2D([[4, 5, 6, 5], [5, 6, 7, 5], [2, 3, 4, 5], [2, 3, 4, 4]], "level2"),
                  GameLevel2D([[5, 6, 7, 6], [6, 7, 8, 6], [2, 3, 4, 6], [2, 3, 4, 4]], "level3"),
                  GameLevel2D([[3, 2, 1, 6], [6, 7, 8, 6], [2, 3, 4, 6], [2, 3, 4, 4]], "level4"),
                  GameLevel2D([[9, 2, 7, 3], [6, 7, 8, 3], [2, 3, 4, 3], [2, 3, 4, 4]], "level5")]
        start = time.time()
        a = behavior_diversity(levels, total_symmetry)
        end = time.time()
        print(end - start)


if __name__ == '__main__':
    unittest.main()
