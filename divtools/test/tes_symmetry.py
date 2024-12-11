from divtools.model.game_level_2d import GameLevel2D
from symmetry import horizontal_symmetry
from symmetry import vertical_symmetry
from symmetry import total_symmetry


class Test_Symmetry:
    def test_horizontal_symmetry(self):
        sample_level1 = GameLevel2D([[1, 2, 3], [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4],
                                     [2, 5, 4],
                                     [1, 2, 6]])
        sample_level3 = GameLevel2D([[0], [0]])
        assert horizontal_symmetry(sample_level1) == 0
        assert horizontal_symmetry(sample_level2) == 4
        assert horizontal_symmetry(sample_level3) == 1

    def test_vertical_symmetry(self):
        sample_level1 = GameLevel2D([[3, 3, 6, 4, 4, 4, 4, 4, 2, 2]])
        sample_level2 = GameLevel2D([[2, 2, 4, 4, 0, 0, 3, 5, 2, 4],
                                     [3, 3, 6, 4, 2, 2, 4, 4, 2, 2]])
        sample_level3 = GameLevel2D([[0, 0]])

        assert vertical_symmetry(sample_level1) == 2
        assert vertical_symmetry(sample_level2) == 4
        assert vertical_symmetry(sample_level3) == 1

    def test_total_symmetry(self):
        sample_level1 = GameLevel2D(
            [[1, 2, 3, 5, 5, 3, 1, 3, 4, 5],
             [1, 4, 4, 5, 4, 6, 5, 6, 5, 4],
             [6, 4, 2, 3, 4, 5, 2, 1, 2, 3],
             [6, 5, 4, 5, 3, 4, 3, 2, 6, 2],
             [2, 1, 2, 6, 5, 3, 6, 2, 2, 2],
             [2, 1, 2, 1, 2, 1, 5, 6, 3, 1],
             [2, 5, 3, 3, 4, 2, 5, 6, 2, 6],
             [4, 5, 5, 4, 6, 5, 6, 6, 5, 1],
             [2, 6, 3, 1, 6, 1, 6, 5, 1, 5],
             [5, 1, 3, 1, 6, 1, 6, 3, 6, 3]])

        assert total_symmetry(sample_level1) == 14
