# -*- encoding: utf-8 -*-

import unittest

import merging_rules as m

class TestMergingRules(unittest.TestCase):

    def test_take_all_empty(self):
        # Two empty field lists. 
        fields1 = []
        fields2 = []
        self.assertEqual(m.take_all(fields1, fields2, '970'), [])
        # One empty field lists. 
        fields2 = [([('o', '0003717PHOPHO')], 'C', '0', '', 18)]
        self.assertEqual(m.take_all(fields1, fields2, '970'), fields2)

    def test_take_all(self):
        fields1 = [([('a', '0003717BABA')], '', '', '', 8)]
        fields2 = [([('o', '0003717PHOPHO')], 'C', '0', '', 18)]
        out = [ ([('a', '0003717BABA')], '', '', '', 8), ([('o', '0003717PHOPHO')], 'C', '0', '', 18)]
        self.assertEqual(m.take_all(fields1, fields2, '970'), out)
        # Now for a more tricky one where only the field position changes.
        fields2 = [([('a', '0003717BABA')], '', '', '', 9)]
        out = [ ([('a', '0003717BABA')], '', '', '', 8)]
        self.assertEqual(m.take_all(fields1, fields2, '970'), out)
    def test_take_all_same_field_different_origin(self):
        fields1 = [([('a', '2011ApJ...741...91C'), ('2', 'ADS bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
                   ([('y', '2011arXiv1103.2570C'), ('2', 'eprint bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
                   ([('a', 'arXiv:1103.2570'), ('2', 'arXiv'), ('8', 'ADS metadata')], ' ', ' ', '', 4)]
        fields2 = [([('a', '2011ApJ...741...91C'), ('2', 'ADS bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 2), 
                   ([('a', 'arXiv:1103.2570'), ('2', 'arXiv'), ('8', 'ARXIV')], ' ', ' ', '', 3)]
        out = [([('a', '2011ApJ...741...91C'), ('2', 'ADS bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
               ([('y', '2011arXiv1103.2570C'), ('2', 'eprint bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
               ([('a', 'arXiv:1103.2570'), ('2', 'arXiv'), ('8', 'ADS metadata')], ' ', ' ', '', 4)]
        self.assertEqual(m.take_all(fields1, fields2, '035'), out)


if __name__ == '__main__':
    unittest.main()
