# -*- encoding: utf-8 -*-

import sys
sys.path.append('../')
import unittest

import merger.merging_rules as m
import pipeline_settings
from merger.merger_errors import EqualOrigins, EqualFields

import logging
logging.basicConfig(format=pipeline_settings.LOGGING_FORMAT)
logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME)
logger.setLevel(logging.ERROR)

class TestMergingRules(unittest.TestCase):
    ####################
    #test of get_trusted_and_untrusted_fields
    def test_get_trusted_and_untrusted_fields_1(self):
        #two different fields
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)]
        out =([([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)],
              [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)])
        self.assertEqual(m.get_trusted_and_untrusted_fields(fields1, fields2, '100'), out)
    def test_get_trusted_and_untrusted_fields_2(self):
        #same field with different origins with different priority
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        out = ([([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)],
               [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)])
        self.assertEqual(m.get_trusted_and_untrusted_fields(fields1, fields2, '100'), out)
    def test_get_trusted_and_untrusted_fields_3(self):
        #same field with different origin having the same priority
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        self.assertRaises(EqualOrigins, m.get_trusted_and_untrusted_fields, fields1, fields2, '100')
    def test_get_trusted_and_untrusted_fields_4(self):
        #two different fields with same origin
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)]
        self.assertRaises(EqualOrigins, m.get_trusted_and_untrusted_fields, fields1, fields2, '100')
    def test_get_trusted_and_untrusted_fields_5(self):
        #exactly same field
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        self.assertRaises(EqualOrigins, m.get_trusted_and_untrusted_fields, fields1, fields2, '100')
    ####################
    #test of _get_best_fields
    def test_get_best_fields(self):
        #exactly same field
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        out = ([([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)],
               [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)])
        self.assertEqual(m._get_best_fields(fields1, fields2, '100'), out)
    def test_get_best_fields_1(self):
        #same field with different origin
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        out = ([([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31)], 
               [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)])
        self.assertEqual(m._get_best_fields(fields1, fields2, '100'), out)
    def test_get_best_fields_2(self):
        #same origin different number of fields
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1965fake...91....1K'), ('e', '1'), ('b', '1965fake...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        out = ([([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                ([('i', '1965fake...91....1K'), ('e', '1'), ('b', '1965fake...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)],
               [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)])
        self.assertEqual(m._get_best_fields(fields1, fields2, '100'), out)
    def test_get_best_fields_3(self):
        #different origin and different number of fields
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31),
                   ([('i', '1965fake...91....1K'), ('e', '1'), ('b', '1965fake...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        out = ([([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31),
                ([('i', '1965fake...91....1K'), ('e', '1'), ('b', '1965fake...91....1K'), ('8', 'BAAA')], 'C', '5', '', 31)],
               [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)])
        self.assertEqual(m._get_best_fields(fields1, fields2, '100'), out)
    def test_get_best_fields_4(self):
        #two different fields with same origin and different number of subfields
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI'), ('f', 'FOO')], 'C', '5', '', 31)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)]
        out = ([([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI'), ('f', 'FOO')], 'C', '5', '', 31)],
               [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)])
        self.assertEqual(m._get_best_fields(fields1, fields2, '100'), out)
    def test_get_best_fields_5(self):
        #two different fields with same origin and same number of subfields but different length of the subfields strings
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)]
        out = ([([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1')], 'C', '5', '', 22)],
               [([('i', '1965IBVS...91....1K'), ('e', '1'), ('b', '1965IBVS...91....1K'), ('8', 'ISI')], 'C', '5', '', 31)])
        self.assertEqual(m._get_best_fields(fields1, fields2, '100'), out)
    def test_get_best_fields_6(self):
        #two different fields with same origin and same number of subfields and same length of the subfields strings but different content of the strings
        fields1 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, FOO'), ('e', '1')], 'C', '5', '', 22)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, BAR'), ('e', '1')], 'C', '5', '', 22)]
        self.assertRaises(EqualFields, m._get_best_fields, fields1, fields2, '100')
    ####################
    #tests of the actual merging functions
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
    
    def test_reference_merger_1(self):
        #simple merge between two reference list tht have to be merged
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31)]
        fields2 = [([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
               ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22)]
        self.assertEqual(sorted(m.references_merger(fields1, fields2, '999')), sorted(out))
    
    def test_reference_merger_2(self):
        #simple merge between two incomplete lists and a complete one
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22)]
        fields2 = [([('i', '1964IBVS...54....1S'), ('e', '1'), ('f', 'OCR'), ('b', 'Strohmeier, W.:1964, Inf Bull Var. Stars No. 54'), ('8', 'OCR')], 'C', '5', '', 35)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
               ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
               ([('i', '1964IBVS...54....1S'), ('e', '1'), ('f', 'OCR'), ('b', 'Strohmeier, W.:1964, Inf Bull Var. Stars No. 54'), ('8', 'OCR')], 'C', '5', '', 35)]
        self.assertEqual(sorted(m.references_merger(fields1, fields2, '999')), sorted(out))
    
    def test_reference_merger_3(self):    
        #merging of two incomplete lists (AUTHOR and ISI) and two complete (OCR and PUBLISHER) there must be priority between the complete lists and take_all with the other group
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1964IBVS...54....1S'), ('e', '1'), ('f', 'OCR'), ('b', 'Strohmeier, W.:1964, Inf Bull Var. Stars No. 54'), ('8', 'OCR')], 'C', '5', '', 35)]
        fields2 = [([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        self.assertEqual(sorted(m.references_merger(fields1, fields2, '999')), sorted(out))
    def test_reference_merger_4(self):
        #merging of two lists with the same reference but with the less trusted origin having better metadata
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'CROSSREF'), ('b', 'Kohler, U.: Photometric Light-Curves of Southern BV-Stars 1965'), ('8', 'CROSSREF')], 'C', '5', '', 31)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', 'Kohler, U.: Photometric Light-Curves of Southern BV-Stars 1965'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        merged = m.references_merger(fields1, fields2, '999')
        self.assertEqual([(sorted(elem[0]),)+elem[1:] for elem in sorted(merged)], [(sorted(elem[0]),)+elem[1:] for elem in sorted(out)])
    
    def test_reference_merger_5(self):
        #merging of two lists with the same reference but with the less trusted origin having better metadata and an reference extension
        fields1 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', '1965IBVS...91....1K'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        fields2 = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'CROSSREF'), ('b', 'Kohler, U.: Photometric Light-Curves of Southern BV-Stars 1965'), ('w', 'iop.xml'), ('8', 'CROSSREF')], 'C', '5', '', 31)]
        out = [([('i', '1965IBVS...91....1K'), ('e', '1'), ('f', 'AUTHOR'), ('b', 'Kohler, U.: Photometric Light-Curves of Southern BV-Stars 1965'), ('w', 'iop.xml'), ('8', 'AUTHOR')], 'C', '5', '', 31),
                   ([('i', '1982A&A...105..389V'), ('8', 'ISI'), ('b', 'Van Hamme, W.:1982, Astron. Astrophys. 105, 389'), ('e', '1'), ('f', 'ISI')], 'C', '5', '', 22),
                   ([('i', '1974IBVS..888....1C'), ('e', '1'), ('f', 'PUBLISHER'), ('b', 'Castore de Sister6, M.E., Sister6, R.F.:1974, Inf Bull Var. Stars No. 888'), ('8', 'PUBLISHER')], 'C', '5', '', 27)]
        merged = m.references_merger(fields1, fields2, '999')
        self.assertEqual([(sorted(elem[0]),)+elem[1:] for elem in sorted(merged)], [(sorted(elem[0]),)+elem[1:] for elem in sorted(out)])

if __name__ == '__main__':
    unittest.main()
