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


class TestBoxPlot(svgTest):

    def test_should_have_correct_fields(self):
        coll = plots.boxplot(list(range(20)), 0, 1)
        self.assertSetEqual(set(coll.keys()),
                            {'box', 'whiskers', 'median'})
