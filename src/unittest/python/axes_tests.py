from unittest import mock

import svgwrite

from pypl.testing import svgTest
from pypl import axes


class TestGetTicks(svgTest):

    def setUp(self):
        self.scl = mock.Mock()
        self.scl.data_0 = 0
        self.scl.data_len = 5

    def test_should_return_correct_number_of_ticks(self):
        ticks = axes.get_ticks(self.scl, 5)
        self.assertEqual(len(ticks), 5)


class TestVAxis(svgTest):

    runfor = [axes.vaxis, axes.haxis]

    def setUp(self):
        self.scl = mock.Mock()
        self.scl.data_0 = 0
        self.scl.data_len = 5
        self.scl.side_effect = lambda x: x

    def test_should_have_nticks_plus_1_line_elements(self):
        for cmd in self.runfor:
            with self.subTest(cmd=cmd):
                ax = cmd(self.scl, 5)
                line_elements = [el for el in ax.elements
                                 if isinstance(el, svgwrite.shapes.Line)]
                self.assertEqual(len(line_elements), 6)

    def test_should_add_label_is_given(self):
        for cmd in self.runfor:
            with self.subTest(cmd=cmd):
                ax = cmd(self.scl, 5, label="ANY_LABEL")
                self.assertIn('label', ax)

    def test_all_lines_should_have_numeric_coordinates(self):
        line_attrs = ['x1', 'x2', 'y1', 'y2']
        for cmd in self.runfor:
            with self.subTest(cmd=cmd):
                ax = cmd(self.scl, 5)
                for line in ax.select('line', 'ticks').elements:
                    self.assert_numeric_attributes(line, line_attrs)


class TestTufte(svgTest):

    runfor = [axes.vtufte, axes.htufte]

    def setUp(self):
        self.scl = mock.Mock()
        self.scl.data_0 = 0
        self.scl.data_len = 5
        self.scl.side_effect = lambda x: x

    def test_should_have_exactly_5_ticklabels_but_no_ticks(self):
        data = list(range(20))
        for cmd in self.runfor:
            with self.subTest(cmd=cmd):
                ax = cmd(data, self.scl)
                self.assertEqual(len(ax['ticks']), 0)
                self.assertEqual(len(ax['ticklabels']), 5)

    def test_lines_should_have_valid_coordinates(self):
        data = list(range(20))
        for cmd in self.runfor:
            with self.subTest(cmd=cmd):
                ax = cmd(data, self.scl)
                for l in ax['lines']:
                    self.assert_numeric_attributes(l, ['x1', 'x2', 'y1', 'y2'])
