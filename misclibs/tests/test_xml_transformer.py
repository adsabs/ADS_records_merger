# coding=UTF-8
# Copyright (C) 2011, The SAO/NASA Astrophysics Data System
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
@author: Giovanni Di Milia and Benoit Thiell
File containing tests for the xml_transformer
'''

import sys
sys.path.append('../')
sys.path.append('../../')
import unittest
import libxml2, libxslt
import re

import xml_transformer as x
from invenio import bibrecord

def get_result_invenio_xmltransformer(xmlstring):
    xmlobj = libxml2.parseDoc(xmlstring)
    xslt = '../../misc/AdsXML2MarcXML_v2.xsl'
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(xslt))
    xml_transformed_object = stylesheet.applyStylesheet(xmlobj, None)
    marcxml = xml_transformed_object.serialize(encoding='utf-8')
    #result with internal function
    result_xml_transformer = x.create_record_from_libxml_obj(xml_transformed_object)
    #result with function from invenio
    regex = re.compile('<collection>.*?</collection>', re.DOTALL)
    record_xmls = regex.findall(marcxml)
    result_invenio = [[res[0] for res in bibrecord.create_records(xml)] for xml in record_xmls]
    
    return (result_xml_transformer, result_invenio)


class TestXMLTransformer(unittest.TestCase):
    """ All tests"""
    def test_1_create_record_from_libxml_obj(self):
        xmlstring = '<?xml version="1.0" encoding="UTF-8"?><records><record bibcode="1057QB46.C48......."><metadata type="general" origin="LOC">\
            <creation_time>2012-04-27T13:34:58</creation_time><modification_time>2012-04-27T13:34:58</modification_time><bibcode>1057QB46.C48.......</bibcode>\
            <arxivcategories/><title>Wei jen lei fu wu ti t\'ien wen hsueh.</title><journal>Wei jen lei fu wu ti t\'ien wen hsueh, 1057.</journal><dates>\
            <date type="date-published">1057-00-00</date></dates><comment origin="ADS">LCCN: c59-2999 (PREM);</comment><abstract lang="en">Not Available</abstract>\
            </metadata><metadata type="properties" origin="ADS metadata"><JSON_timestamp>{"abs":[{"p":"/proj/ads/abstracts/ast/text/J57/J57-00529.abs","t":"1335548098"}]}</JSON_timestamp>\
            </metadata></record></records>'
        
        result_xml_transformer, result_invenio = get_result_invenio_xmltransformer(xmlstring)
        self.assertEqual(result_xml_transformer, result_invenio)
        
    def test_2_create_record_from_libxml_obj(self):
        xmlstring = open('xmlfiles/test_2_create_record_from_libxml_obj.xml', 'r').read()
        result_xml_transformer, result_invenio = get_result_invenio_xmltransformer(xmlstring)
        self.assertEqual(result_xml_transformer, result_invenio)
        
    def test_3_create_record_from_libxml_obj(self):
        xmlstring = open('xmlfiles/test_3_create_record_from_libxml_obj.xml', 'r').read()
        result_xml_transformer, result_invenio = get_result_invenio_xmltransformer(xmlstring)
        self.assertEqual(result_xml_transformer, result_invenio)


if __name__ == '__main__':
    unittest.main()