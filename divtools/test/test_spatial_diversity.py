import unittest
from divtools.diversity.spatial_diversity import spatial_diversity
from divtools.model.game_level_2d import GameLevel2D
from divtools.common.utils import match_args


class TestSpatialDiversity(unittest.TestCase):
    levels = [GameLevel2D([[1, 2, 3], [2, 3, 4]]) for _ in range(5)]

    # All gaps are placed in the one segment.
    @match_args
    def feature_metric_stub(self, levels):
        return [5, 0, 0, 0, 0]

    # Gaps are placed in all level segments uniformly.
    @match_args
    def feature_metric_stub_2(self, levels):
        return [1, 1, 1, 1, 1]

    # test calculate spatial diversity
    def test_spatial_diversity_with_valid_input(self):
        result = spatial_diversity(self.levels, self.feature_metric_stub)
        self.assertEqual(len(result), 5)
        self.assertEqual(result, [0.0, 0.0, 0.0, 0.0, 0.0])
        result = spatial_diversity(self.levels, self.feature_metric_stub_2)
        for a, b in zip(result, [1, 1, 1, 1, 1]):
            self.assertAlmostEqual(a, b, delta=0.0001)

    # empty levels
    def test_spatial_diversity_with_empty_levels(self):
        levels = []
        result = spatial_diversity(levels, self.feature_metric_stub)
        self.assertEqual(result, [])

    # feature metric is None
    def test_spatial_diversity_with_none_feature_metric(self):
        with self.assertRaises(TypeError):
            spatial_diversity(self.levels, None)

    # feature metric is invalid
    def test_spatial_diversity_with_invalid_feature_metric(self):
        with self.assertRaises(TypeError):
            spatial_diversity(self.levels, "invalid")


if __name__ == '__main__':
    unittest.main()
