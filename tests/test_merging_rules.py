# -*- encoding: utf-8 -*-

import sys
sys.path.append('../')
sys.path.append('/proj/ads/soft/python/lib/site-packages')
sys.path.append('/proj/adsx/invenio/lib/python')

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


if __name__ == '__main__':
    unittest.main()
