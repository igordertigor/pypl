import unittest
from unittest import mock

from pypl import plots


class TestElementsCollection(unittest.TestCase):

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
