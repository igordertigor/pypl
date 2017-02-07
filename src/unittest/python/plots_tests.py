from unittest import mock

import svgwrite

from pypl.testing import svgTest
from pypl import plots


class TestElementsCollection(svgTest):

    def test_elements_should_contain_all_elements(self):
        coll = plots.ElementsCollection()
        coll['ANY_GROUP'].append('ANY_PLOT_ELEMENT')
        coll['ANY_OTHER_GROUP'].append('ANY_OTHER_PLOT_ELEMENT')
        self.assertSetEqual(set(coll.elements),
                            {'ANY_PLOT_ELEMENT', 'ANY_OTHER_PLOT_ELEMENT'})

    def test_attr_should_be_chainable(self):
        mock_svg_element = mock.Mock()
        mock_svg_element.attribs = {}

        coll = plots.ElementsCollection()
        coll['ANY_GROUP'].append(mock_svg_element)

        coll.attr('ANY_ATTRIBUTE', 2)

        self.assertIn('ANY_ATTRIBUTE', mock_svg_element.attribs)
        self.assertEqual(mock_svg_element.attribs['ANY_ATTRIBUTE'], 2)

    def test_select_should_return_new_collection(self):
        coll = plots.ElementsCollection()
        coll['ANY_GROUP'].append('ANY_ELEMENT')
        coll['ANY_OTHER_GROUP'].append('ANY_OTHER_ELEMENT')

        newcoll = coll.select('ANY_GROUP')
        self.assertSetEqual(set(newcoll.keys()), {'ANY_GROUP'})

    def test_setting_on_selection_should_modify_original_collection(self):
        mock_svg_element = mock.Mock()
        mock_svg_element.attribs = {}

        coll = plots.ElementsCollection()
        coll['ANY_GROUP'].append(mock_svg_element)

        coll.select('ANY_GROUP').attr('ANY_ATTRIBUTE', 2)

        self.assertIn('ANY_ATTRIBUTE', mock_svg_element.attribs)
        self.assertEqual(mock_svg_element.attribs['ANY_ATTRIBUTE'], 2)

    def test_add_should_combine_both_summands(self):
        coll1 = plots.ElementsCollection()
        coll1['ANY_GROUP'].append('ANY_ELEMENT')
        coll1['ANY_OTHER_GROUP'].append('ANY_OTHER_ELEMENT')
        coll2 = plots.ElementsCollection()
        coll2['ANY_GROUP'].append('ANY_THIRD_ELEMENT')
        coll2['YET_ANOTHER_GROUP'].append('YET_ANOTHER_ELEMENT')

        coll3 = coll1 + coll2

        self.assertSetEqual(
            set(coll3.keys()),
            {'ANY_GROUP', 'ANY_OTHER_GROUP', 'YET_ANOTHER_GROUP'})
        self.assertSetEqual(set(coll3['ANY_GROUP']),
                            {'ANY_ELEMENT', 'ANY_THIRD_ELEMENT'})
        self.assertSetEqual(set(coll3['ANY_OTHER_GROUP']),
                            {'ANY_OTHER_ELEMENT'})
        self.assertSetEqual(set(coll3['YET_ANOTHER_GROUP']),
                            {'YET_ANOTHER_ELEMENT'})


class TestToSVGElements(svgTest):

    def setUp(self):
        self.coll = plots.ElementsCollection()
        self.coll['ANY_GROUP'].append('ANY_ELEMENT')
        self.coll['ANY_OTHER_GROUP'].append('ANY_OTHER_ELEMENT')
        self.target = mock.Mock()
        self.target.elements = []

    def test_to_svg_elements_should_add_to_target_in_any_order(self):
        self.coll.to_svg_elements(self.target)

        self.assertSetEqual(set(self.target.elements),
                            {'ANY_ELEMENT', 'ANY_OTHER_ELEMENT'})

    def test_to_svg_elements_should_add_to_target_in_order(self):
        self.coll.to_svg_elements(self.target,
                                  ['ANY_OTHER_GROUP', 'ANY_GROUP'])

        self.assertEqual(self.target.elements,
                         ['ANY_OTHER_ELEMENT', 'ANY_ELEMENT'])

    def test_to_svg_elements_should_allow_filtering(self):
        self.coll.to_svg_elements(self.target, ['ANY_GROUP'])

        self.assertSetEqual(set(self.target.elements),
                            {'ANY_ELEMENT'})


class TestScatterPlot(svgTest):

    def test_should_create_circle_elements_per_data_point(self):
        coll = plots.scatterplot([0], [1, 2], ['#000'])

        points = [e for e in coll['points']
                  if isinstance(e, svgwrite.shapes.Circle)]
        self.assertEqual(len(points), 2)

    def test_should_add_correct_colors_to_circles(self):
        coll = plots.scatterplot([0], [1, 2], ['#000', '#e2a'])

        pointcolors = [e.attribs['fill'] for e in coll['points']
                       if isinstance(e, svgwrite.shapes.Circle)]

        self.assertSetEqual(set(pointcolors),
                            {'#000', '#e2a'})

    def test_should_have_numeric_values_for_circle_locations(self):
        coll = plots.scatterplot([0], [1, 2], ['#000'])

        for point in coll['points']:
            self.assert_numeric_attributes(point, ['cy', 'cx', 'r'])


class TestBoxPlot(svgTest):

    def setUp(self):
        self.scl = mock.Mock()
        self.scl.data_0 = 0
        self.scl.data_len = 5
        self.scl.side_effect = lambda x: x

    def test_should_have_correct_fields(self):
        coll = plots.boxplot(list(range(20)), self.scl, 0, 1)
        self.assertSetEqual(set(coll.keys()),
                            {'box', 'whiskers', 'median'})

    def test_should_have_numeric_values_for_plot_elements(self):
        coll = plots.boxplot(list(range(20)), self.scl, 0, 1)
        for line in coll.select('whiskers', 'median').elements:
            self.assert_numeric_attributes(line, ['x1', 'x2', 'y1', 'y2'])

        box = coll['box'][0]
        self.assert_numeric_attributes(box, ['width', 'height', 'x', 'y'])


class TestLegend(svgTest):

    def test_should_have_numeric_values_for_text_and_markers(self):
        coll = plots.legend({'a': '#000', 'b': '#efa'}, (10, 10), 10, 5)
        for label in coll['labels']:
            self.assert_numeric_attributes(label, ['x', 'y'])

        for marker in coll['fields']:
            self.assert_numeric_attributes(marker,
                                           ['x', 'y', 'width', 'height'])

    def test_should_have_circles_if_marker_is_circle(self):
        coll = plots.legend({'a': '#000', 'b': '#efa'}, (10, 10), 10, 5,
                            svgwrite.shapes.Circle)
        for marker in coll['fields']:
            self.assertIsInstance(marker, svgwrite.shapes.Circle)
            self.assert_numeric_attributes(marker,
                                           ['cx', 'cy', 'r'])

    def test_should_have_lines_if_marker_is_line(self):
        coll = plots.legend({'a': '#000', 'b': '#efa'}, (10, 10), 10, 5,
                            svgwrite.shapes.Line)
        for marker in coll['fields']:
            self.assertIsInstance(marker, svgwrite.shapes.Line)
            self.assert_numeric_attributes(marker,
                                           ['x1', 'x2', 'y1', 'y1'])


class TestErrorLine(svgTest):

    def test_line_should_have_numeric_coordinates(self):
        lines = plots.errorline((range(4), range(4)))
        for line in lines['line']:
            self.assert_numeric_paths(line, ['points'])

    def test_points_should_have_numeric_coordinages(self):
        lines = plots.errorline((range(4), range(4)))
        for point in lines['markers']:
            self.assert_numeric_attributes(point, ['cx', 'cy', 'r'])

    def test_should_not_create_points_if_mark_is_false(self):
        lines = plots.errorline((range(4), range(4)), mark=False)
        self.assertNotIn('markers', lines)

    def test_should_create_polygon_if_ci_is_specified(self):
        lines = plots.errorline((range(4), range(4)),
                                ci=(range(-1, 3), range(1, 5)))
        self.assertIn('ci', lines)
        for ci in lines['ci']:
            self.assertIsInstance(ci, svgwrite.shapes.Polygon)
            self.assert_numeric_paths(ci, ['points'])


class TestBars(svgTest):

    def test_should_have_numeric_coordinates(self):
        bars = plots.bars((range(4), [1, 2, 1, 1]), .6, 0.)
        for bar in bars['bars']:
            self.assert_numeric_attributes(bar, ['x', 'y', 'width', 'height'])
