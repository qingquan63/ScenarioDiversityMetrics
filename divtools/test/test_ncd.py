from divtools.model.game_level_2d import GameLevel2D
from divtools.diversity.ncd import ncd


class Test_NCD:
    def test_ncd(self):
        sample_level1 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4],
                                     [2, 5, 4],
                                     [1, 2, 6]])
        sample_level3 = GameLevel2D([[0], [0]])
        assert ncd(sample_level1, sample_level2) - 0.28 < 0.01
        assert ncd(sample_level2, sample_level3) - 0.50 < 0.01
        assert ncd(sample_level1, sample_level3) - 0.29 < 0.01
