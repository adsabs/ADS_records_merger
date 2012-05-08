# -*- encoding: utf-8 -*-
import sys
sys.path.append('../')

import unittest

import basic_functions as b

class TestBasicFunctions(unittest.TestCase):

    def test_is_unicode(self):
        self.assertEqual(b.is_unicode(''), False)
        self.assertEqual(b.is_unicode('abc'), False)
        self.assertEqual(b.is_unicode('élève'), True)

    def test_is_mostly_uppercase(self):
        self.assertEqual(b.is_mostly_uppercase('THIS IS ALL UPPERCASE.'), True)
        self.assertEqual(b.is_mostly_uppercase('THIS IS ALL UPPERCASE WITH 1 NUMBER.'), True)
        self.assertEqual(b.is_mostly_uppercase('This Is Camel Case.'), False)
        self.assertEqual(b.is_mostly_uppercase('This is mostly lowercase.'), False)

    def test_month_in_date(self):
        self.assertEqual(b.month_in_date('01/1998'), True)
        self.assertEqual(b.month_in_date('00/1998'), False)
        self.assertEqual(b.month_in_date('01/01/1998'), False)
        self.assertEqual(b.month_in_date('1/1/1998'), False)
        self.assertEqual(b.month_in_date('1/1998'), False)
        self.assertEqual(b.month_in_date('1998/01'), False)
        self.assertEqual(b.month_in_date('1998/01/01'), False)

    def test_get_origin(self):
        pass

    def test_get_origin_value(self):
        pass

if __name__ == '__main__':
    unittest.main()
