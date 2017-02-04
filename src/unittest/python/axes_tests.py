import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import svgwrite

from pypl import utils
from pypl import axes


class TestGetTicks(unittest.TestCase):

    def setUp(self):
        self.scl = mock.Mock()
        self.scl.data_0 = 0
        self.scl.data_len = 5

    def test_should_return_correct_number_of_ticks(self):
        ticks, raw = axes.get_ticks(self.scl, 5)
        self.assertEqual(len(ticks), 5)
        self.assertEqual(len(raw), 5)

    def test_should_call_scl_for_each_tick(self):
        self.scl.side_effect = list(range(5))

        axes.get_ticks(self.scl, 5)

        self.assertEqual(self.scl.call_count, 5)


class TestVAxis(unittest.TestCase):

    runfor = [axes.vaxis, axes.haxis]

    def setUp(self):
        self.scl = mock.Mock()
        self.scl.data_0 = 0
        self.scl.data_len = 5
        self.scl.side_effect = list(range(20))

    def test_should_have_nticks_plus_1_line_elements(self):
        for cmd in self.runfor:
            with self.subTest(cmd=cmd):
                ax = cmd(self.scl, 5)
                line_elements = [el for el in utils.all_elements(ax)
                                 if isinstance(el, svgwrite.shapes.Line)]
                self.assertEqual(len(line_elements), 6)
