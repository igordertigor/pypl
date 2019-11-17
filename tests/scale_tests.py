import unittest

from pypl import scale


class TestContinuousScale(unittest.TestCase):

    def test_should_return_smallest_value_when_called_with_minval(self):
        s = scale.ContinuousScale((2, 5), (0, 3))

        self.assertEqual(s(2), 0)

    def test_should_return_largest_value_when_called_with_maxval(self):
        s = scale.ContinuousScale((2, 5), (0, 3))

        self.assertEqual(s(5), 3)

    def test_should_give_inverted_scale_when_called_with_inverted_range(self):
        s = scale.ContinuousScale((2, 5), (3, 0))

        self.assertEqual(s(2), 3)
        self.assertEqual(s(5), 0)


class TestCategoricalScale(unittest.TestCase):

    def test_should_return_uniform_values_in_target_interval(self):
        data = ['foo', 'bar', 'foo', 'foo', 'bar', 'baz']
        s = scale.CategoricalScale(data, (0, 3))

        mx, mn = 0, 3
        for d in data:
            sd = s(d)
            self.assertGreaterEqual(sd, 0)
            self.assertLessEqual(sd, 3)
            self.assertIsInstance(sd, float)
            mx = max(mx, sd)
            mn = min(mn, sd)

        # span the whole range
        self.assertEqual(mn, 0)
        self.assertEqual(mx, 3)
