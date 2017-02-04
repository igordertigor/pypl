import unittest

from pypl import plots


class TestElementsCollection(unittest.TestCase):

    def test_elements_should_contain_all_elements(self):
        coll = plots.ElementsCollection()
        coll['ANY_GROUP'].append('ANY_PLOT_ELEMENT')
        coll['ANY_OTHER_GROUP'].append('ANY_OTHER_PLOT_ELEMENT')
        self.assertSetEqual(set(coll.elements),
                            {'ANY_PLOT_ELEMENT', 'ANY_OTHER_PLOT_ELEMENT'})
