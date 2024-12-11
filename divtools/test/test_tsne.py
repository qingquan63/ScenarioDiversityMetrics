import unittest
from divtools.model.game_level_2d import GameLevel2D
from divtools.graph.tsne_visualization import tsne_visualization


class MyTestCase(unittest.TestCase):
    def test_draw(self):
        levels = [GameLevel2D([[1, 2, 3], [2, 3, 4]], "level1"),
                  GameLevel2D([[2, 3, 4], [3, 4, 5]], "level1"),
                  GameLevel2D([[3, 4, 5], [4, 5, 6]], "level2"),
                  GameLevel2D([[4, 5, 6], [5, 6, 7]], "level2"),
                  GameLevel2D([[5, 6, 7], [6, 7, 8]], "level3"),
                  GameLevel2D([[3, 2, 1], [6, 7, 8]], "level4"),
                  GameLevel2D([[9, 2, 7], [6, 7, 8]], "level5")]

        tsne_visualization(levels)


if __name__ == '__main__':
    unittest.main()
