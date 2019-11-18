import unittest
from unittest import mock

from pypl import utils


class TestPrctile(unittest.TestCase):

    def test_should_return_perctiles_on_range_10(self):
        data = [1, 2, 5, 3, 10, 9, 8, 4, 6, 7]
        p = utils.prctiles(data)

        expected = {1, 3, 5, 7, 10}
        self.assertSetEqual(set(p), expected)

    def test_should_return_prctiles_on_range_3(self):
        data = [2, 1, 3]
        p = utils.prctiles(data)

        expected = [1, 1, 2, 2, 3]
        self.assertEqual(p, expected)


class TestClip(unittest.TestCase):

    def test_clipping_should_affect_all_points_outside_the_range(self):
        scl = mock.Mock()
        scl.data_0 = 0
        scl.data_len = 1

        clipped = utils.clip([-1, 1, 0, 2], scl)

        self.assertEqual(clipped, [0, 1, 0, 1])
