from divtools.model.game_level_2d import GameLevel2D
from similarity import get_similar_rows
from similarity import get_similar_cols
from similarity import similarity


class Test_Similarity:
    def test_get_similar_rows(self):
        sample_level1 = GameLevel2D([[1, 2, 3], [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3], [2, 3, 6]])
        sample_level3 = GameLevel2D([[1, 2, 3], [2, 3, 4]])
        sample_level4 = GameLevel2D([[2, 1, 3], [5, 3, 4]])
        test_set = [sample_level1, sample_level2, sample_level3, sample_level4]

        assert get_similar_rows(test_set) == {(1, 2, 3), (2, 3, 4), (2, 3, 6), (2, 1, 3), (5, 3, 4)}

    def test_get_similar_cols(self):
        sample_level1 = GameLevel2D([[1, 2, 3], [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3], [2, 3, 6]])
        sample_level3 = GameLevel2D([[1, 2, 3], [3, 3, 4]])
        sample_level4 = GameLevel2D([[2, 1, 3], [5, 3, 4]])
        test_set = [sample_level1, sample_level2, sample_level3, sample_level4]

        assert get_similar_cols(test_set) == {(1, 2), (2, 3), (3, 4), (3, 6), (1, 3), (2, 5)}

    def test_similarity(self):
        sample_level1 = GameLevel2D([[1, 2, 3], [2, 3, 4]])
        sample_level2 = GameLevel2D([[1, 2, 3], [2, 3, 6]])
        sample_level3 = GameLevel2D([[1, 2, 3], [3, 3, 4]])
        sample_level4 = GameLevel2D([[2, 1, 3], [5, 3, 4]])
        test_set = [sample_level1, sample_level2, sample_level3, sample_level4]
        rows = get_similar_rows(test_set)
        cols = get_similar_cols(test_set)
        level_segment1 = GameLevel2D([[1, 2, 3], [2, 6, 5]])
        level_segment2 = GameLevel2D([[2, 2, 4], [2, 6, 5]])
        level_segment3 = GameLevel2D([[2, 3, 3], [2, 6, 4]])

        assert similarity(level_segment1, rows, cols) == 2
        assert similarity(level_segment2, rows, cols) == 0
        assert similarity(level_segment3, rows, cols) == 2
