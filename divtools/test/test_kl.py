import pytest
from divtools.model.game_level_2d import GameLevel2D
from collections import Counter
from divtools.diversity.kl import find_pattern
from divtools.diversity.kl import kl_divergence_2d


class Test_KL:
    def test_find_pattern(self):
        sample_level1 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4],
                                     [2, 5, 4],
                                     [1, 2, 6]])
        sample_level3 = GameLevel2D([[0], [0]])
        assert find_pattern(sample_level1, 2) == Counter({((1, 2), (2, 3)): 1, ((2, 3), (3, 4)): 1})
        assert find_pattern(sample_level2, 2) == Counter({((1, 2), (2, 3)): 1,
                                                          ((2, 3), (3, 4)): 1,
                                                          ((2, 3), (2, 5)): 1,
                                                          ((3, 4), (5, 4)): 1,
                                                          ((2, 5), (1, 2)): 1,
                                                          ((5, 4), (2, 6)): 1})
        assert find_pattern(sample_level3, 1) == Counter({((0,),): 2})

    def test_KL_Divergence_2d(self):
        sample_level1 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 4],
                                     [2, 5, 4],
                                     [1, 2, 6]])

        sample_level4 = GameLevel2D([[1, 2, 3],
                                     [2, 3, 6],
                                     [2, 5, 4],
                                     [2, 2, 6]])

        assert kl_divergence_2d(sample_level2, sample_level1, 2) - 144.1 < 0.1
        assert kl_divergence_2d(sample_level1, sample_level2, 2) == 0

        assert kl_divergence_2d(sample_level2, sample_level4, 2) - 108.1 < 0.1
        assert kl_divergence_2d(sample_level1, sample_level4, 2) - 36.0 < 0.1
