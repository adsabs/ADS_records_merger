# -*- encoding: utf-8 -*-

import sys
sys.path.append('../')
import unittest

import merger.merging_rules as m

class TestMergingRules(unittest.TestCase):

    def test_take_all_empty(self):
        # Two empty field lists. 
        fields1 = []
        fields2 = []
        self.assertEqual(m.take_all(fields1, fields2, '970', False), [])
        # One empty field lists. 
        fields2 = [([('o', '0003717PHOPHO')], 'C', '0', '', 18)]
        self.assertEqual(m.take_all(fields1, fields2, '970', False), fields2)

    def test_take_all(self):
        fields1 = [([('a', '0003717BABA')], '', '', '', 8)]
        fields2 = [([('o', '0003717PHOPHO')], 'C', '0', '', 18)]
        out = [ ([('a', '0003717BABA')], '', '', '', 8), ([('o', '0003717PHOPHO')], 'C', '0', '', 18)]
        self.assertEqual(m.take_all(fields1, fields2, '970', False), out)
        # Now for a more tricky one where only the field position changes.
        fields2 = [([('a', '0003717BABA')], '', '', '', 9)]
        out = [ ([('a', '0003717BABA')], '', '', '', 8)]
        self.assertEqual(m.take_all(fields1, fields2, '970', False), out)
    
    def test_take_all_same_field_different_origin(self):
        fields1 = [([('a', '2011ApJ...741...91C'), ('2', 'ADS bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
                   ([('y', '2011arXiv1103.2570C'), ('2', 'eprint bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
                   ([('a', 'arXiv:1103.2570'), ('2', 'arXiv'), ('8', 'ADS metadata')], ' ', ' ', '', 4)]
        fields2 = [([('a', '2011ApJ...741...91C'), ('2', 'ADS bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 2), 
                   ([('a', 'arXiv:1103.2570'), ('2', 'arXiv'), ('8', 'ARXIV')], ' ', ' ', '', 3)]
        out = [([('a', '2011ApJ...741...91C'), ('2', 'ADS bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
               ([('y', '2011arXiv1103.2570C'), ('2', 'eprint bibcode'), ('8', 'ADS metadata')], ' ', ' ', '', 3), 
               ([('a', 'arXiv:1103.2570'), ('2', 'arXiv'), ('8', 'ADS metadata')], ' ', ' ', '', 4)]
        self.assertEqual(m.take_all(fields1, fields2, '035', False), out)
    
    def test_reference_merger(self):
        #simple merge between two reference list tht have to be merged
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
               ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22)]
        self.assertEqual(sorted(m.references_merger(fields1, fields2, '999', False)), sorted(out))
        
        #simple merge between two incomplete lists and a complete one
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22)]
        fields2 = [([('i', '1964IBVS...54....1S'), ('e', '1'), ('f', 'OCR'), ('b', 'Strohmeier, W.:1964, Inf Bull Var. Stars No. 54'), ('8', 'OCR')], 'C', '5', '', 35)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
               ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
               ([('i', '1964IBVS...54....1S'), ('e', '1'), ('f', 'OCR'), ('b', 'Strohmeier, W.:1964, Inf Bull Var. Stars No. 54'), ('8', 'OCR')], 'C', '5', '', 35)]
        self.assertEqual(sorted(m.references_merger(fields1, fields2, '999', False)), sorted(out))
        
        #merging of two incomplete lists (AUTHOR and ISI) and two complete (OCR and PUBLISHER) there must be priority between the complete lists and take_all with the other group
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1964IBVS...54....1S'), ('e', '1'), ('f', 'OCR'), ('b', 'Strohmeier, W.:1964, Inf Bull Var. Stars No. 54'), ('8', 'OCR')], 'C', '5', '', 35)]
        fields2 = [([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        self.assertEqual(sorted(m.references_merger(fields1, fields2, '999', False)), sorted(out))
        
        #merging of two lists with the same reference but with the less trusted origin having better metadata
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'CROSSREF'), ('b', 'Kohler, U.: Photometric Light-Curves of Southern BV-Stars 1965'), ('8', 'CROSSREF')], 'C', '5', '', 31)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', 'Kohler, U.: Photometric Light-Curves of Southern BV-Stars 1965'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        merged = m.references_merger(fields1, fields2, '999', False)
        self.assertEqual([(sorted(elem[0]),)+elem[1:] for elem in sorted(merged)], [(sorted(elem[0]),)+elem[1:] for elem in sorted(out)])

if __name__ == '__main__':
    unittest.main()
