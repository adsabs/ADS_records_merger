# -*- encoding: utf-8 -*-

import unittest

import merger as m
import invenio.bibrecord as b

class TestPriorityBasedMerger(unittest.TestCase):

    def test_01_merge_two_records_one_field(self):
        """
        PRIORITY: 2 records, 1 field, 2 origins.
        """
        marcxml = """<collection>
  <record>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">10</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">15</subfield>
      <subfield code="8">NED</subfield>
    </datafield>
  </record>
</collection>"""
        expected = """<record>
  <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">10</subfield>
    <subfield code="8">A&amp;A</subfield>
  </datafield>
</record>"""
        records = b.create_records(marcxml)
        merged_record = m.merge(records)
        self.assertEqual(merged_record, b.create_record(expected)[0])

    def test_02_merge_two_records_two_fields(self):
        """
        PRIORITY: 2 records, 4 fields, 4 origins.
        """
        marcxml = """<collection>
  <record>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">10</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
    <datafield tag="773" ind1=" " ind2=" ">
      <subfield code="a">Libération</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="773" ind1=" " ind2=" ">
      <subfield code="a">Le Monde</subfield>
      <subfield code="8">AAS</subfield>
    </datafield>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">15</subfield>
      <subfield code="8">NED</subfield>
    </datafield>
  </record>
</collection>"""
        expected = """<record>
  <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">10</subfield>
    <subfield code="8">A&amp;A</subfield>
  </datafield>
  <datafield tag="773" ind1=" " ind2=" ">
    <subfield code="a">Le Monde</subfield>
    <subfield code="8">AAS</subfield>
  </datafield>
</record>"""
        records = b.create_records(marcxml)
        merged_record = m.merge(records)
        self.assertEqual(merged_record, b.create_record(expected)[0])

    def test_03_merge_two_records_one_different_field(self):
        """
        PRIORITY: 2 records, 2 different fields.
        """
        marcxml = """<collection>
  <record>
    <datafield tag="773" ind1=" " ind2=" ">
      <subfield code="a">Libération</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">15</subfield>
      <subfield code="8">NED</subfield>
    </datafield>
  </record>
</collection>"""
        expected = """<record>
  <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">15</subfield>
    <subfield code="8">NED</subfield>
  </datafield>
  <datafield tag="773" ind1=" " ind2=" ">
    <subfield code="a">Libération</subfield>
    <subfield code="8">STI</subfield>
  </datafield>
</record>"""
        records = b.create_records(marcxml)
        merged_record = m.merge(records)
        self.assertEqual(merged_record, b.create_record(expected)[0])

    def test_04_merge_three_records_two_fields(self):
        """
        3 records, 6 fields, 6 origins.
        """
        marcxml = """<collection>
  <record>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">10</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
    <datafield tag="773" ind1=" " ind2=" ">
      <subfield code="a">Libération</subfield>
      <subfield code="8">STI</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="773" ind1=" " ind2=" ">
      <subfield code="a">Le Monde</subfield>
      <subfield code="8">AAS</subfield>
    </datafield>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">15</subfield>
      <subfield code="8">NED</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="300" ind1=" " ind2=" ">
      <subfield code="a">5</subfield>
      <subfield code="8">ADS metadata</subfield>
    </datafield>
    <datafield tag="773" ind1=" " ind2=" ">
      <subfield code="a">L'Express</subfield>
      <subfield code="8">OCR</subfield>
    </datafield>
  </record>
</collection>"""
        expected = """<record>
  <datafield tag="300" ind1=" " ind2=" ">
    <subfield code="a">5</subfield>
    <subfield code="8">ADS metadata</subfield>
  </datafield>
  <datafield tag="773" ind1=" " ind2=" ">
    <subfield code="a">Le Monde</subfield>
    <subfield code="8">AAS</subfield>
  </datafield>
</record>"""
        records = b.create_records(marcxml)
        merged_record = m.merge(records)
        self.assertEqual(merged_record, b.create_record(expected)[0])

class TestAuthorMerger(unittest.TestCase):

    def test_01_merge_two_records_one_field(self):
        """
        AUTHORS: 2 records, priority.
        """
        marcxml = """<collection>
  <record>
    <datafield tag="100" ind1=" " ind2=" ">
      <subfield code="a">Di Milia, Giovanni</subfield>
      <subfield code="b">Di Milia, G</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
    <datafield tag="700" ind1=" " ind2=" ">
      <subfield code="a">Luker, Jay</subfield>
      <subfield code="b">Luker, J</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
    <datafield tag="700" ind1=" " ind2=" ">
      <subfield code="a">Henneken, Edwin</subfield>
      <subfield code="b">Henneken, E</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="100" ind1=" " ind2=" ">
      <subfield code="a">Dimilia, Giovanni</subfield>
      <subfield code="b">Dimilia, G</subfield>
      <subfield code="8">ARXIV</subfield>
    </datafield>
    <datafield tag="700" ind1=" " ind2=" ">
      <subfield code="a">Luker, Jay</subfield>
      <subfield code="b">Luker, J</subfield>
      <subfield code="8">ARXIV</subfield>
    </datafield>
    <datafield tag="700" ind1=" " ind2=" ">
      <subfield code="a">Henneken, Edwin</subfield>
      <subfield code="b">Henneken, E</subfield>
      <subfield code="8">ARXIV</subfield>
    </datafield>
  </record>
</collection>"""
        expected = """<record>
  <datafield tag="100" ind1=" " ind2=" ">
    <subfield code="a">Di Milia, Giovanni</subfield>
    <subfield code="b">Di Milia, G</subfield>
    <subfield code="8">A&amp;A</subfield>
  </datafield>
  <datafield tag="700" ind1=" " ind2=" ">
    <subfield code="a">Luker, Jay</subfield>
    <subfield code="b">Luker, J</subfield>
    <subfield code="8">A&amp;A</subfield>
  </datafield>
  <datafield tag="700" ind1=" " ind2=" ">
    <subfield code="a">Henneken, Edwin</subfield>
    <subfield code="b">Henneken, E</subfield>
    <subfield code="8">A&amp;A</subfield>
  </datafield>
</record>"""
        records = b.create_records(marcxml)
        merged_record = m.merge(records)
        self.assertEqual(merged_record, b.create_record(expected)[0])

    def test_02_merge_two_records_additional_subfield(self):
        """
        AUTHORS: 2 records, 1 additional subfield.
        """
        marcxml = """<collection>
  <record>
    <datafield tag="100" ind1=" " ind2=" ">
      <subfield code="a">Di Milia, Giovanni</subfield>
      <subfield code="b">Di Milia, G</subfield>
      <subfield code="8">A&amp;A</subfield>
    </datafield>
  </record>
  <record>
    <datafield tag="100" ind1=" " ind2=" ">
      <subfield code="a">Di Milia, Giancarlo</subfield>
      <subfield code="b">Di Milia, G</subfield>
      <subfield code="u">Center for astrophysics</subfield>
      <subfield code="8">ARXIV</subfield>
    </datafield>
  </record>
</collection>"""
        expected = """<record>
  <datafield tag="100" ind1=" " ind2=" ">
    <subfield code="a">Di Milia, Giovanni</subfield>
    <subfield code="b">Di Milia, G</subfield>
    <subfield code="u">Center for astrophysics</subfield>
    <subfield code="8">A&amp;A</subfield>
  </datafield>
</record>"""
        records = b.create_records(marcxml)
        expected_record = b.create_record(expected)[0]
        merged_record = m.merge(records)
        self.assertTrue(b._compare_fields(merged_record['100'][0], expected_record['100'][0], strict=False))

if __name__ == '__main__':
    unittest.main()
