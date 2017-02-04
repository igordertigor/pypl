import unittest


class svgTest(unittest.TestCase):

    def check_numerical(self, svg_element, attributes):
        for att in attributes:
            self.assertIsInstance(svg_element.attribs[att], (int, float))
