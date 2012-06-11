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
File containing an example of the steps that should be taken (and better coded) before using the merger
'''

import libxslt
import libxml2
import logging

import sys
sys.path.append('/proj/ads/soft/python/lib/site-packages')
sys.path.append('/proj/adsx/invenio/lib/python')

from ads.ADSExports import ADSRecords

from invenio.bibformat import record_get_xml
from invenio.dbquery import run_sql

from merger.merger import merge_records_xml
import pipeline_settings
from pipeline_invenio_uploader import bibupload_merger

XSLT = 'misc/AdsXML2MarcXML_v2.xsl'

logging.basicConfig(format=pipeline_settings.LOGGING_FORMAT)
logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME) #I use this name because then I will use the same in the pipeline
logger.setLevel(logging.INFO)
logger.warning('Test for merger')

def merge_bibcodes(bibcodes, print_adsxml=False, print_marcxml=False):
    """
    Returns a merged version of the record identified by bibcode.
    """
    # Extract the record from ADS.
    records = ADSRecords('full', 'XML')
    for bibcode in bibcodes:
        records.addCompleteRecord(bibcode)
    ads_xml_obj = records.export()
    
    if print_adsxml:
        print ads_xml_obj.serialize('UTF-8')
    
    # Convert to MarcXML.
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(XSLT))
    xml_object = stylesheet.applyStylesheet(ads_xml_obj, None)
    
    if print_marcxml:
        print xml_object.serialize('UTF-8')
    
    merged_records, bibcodes_with_problems = merge_records_xml(xml_object)
    return merged_records

def merge_bibcodes_and_upload(bibcodes):
    """function that extracts, merges and uploads a bunch of bibcodes"""
    logger.setLevel(logging.WARNING)
    merged_records = merge_bibcodes(bibcodes)
    bibupload_merger(merged_records, logger)

def print_invenio_xml(bibcodes):
    print '<?xml version="1.0" encoding="UTF-8"?><collection xmlns="http://www.loc.gov/MARC21/slim">'
    for bibcode in bibcodes:
        print '<!-- ################################################################## -->'
        print '<!-- bibcode: %s -->' % bibcode
        ids = run_sql('select id_bibrec from bibrec_bib97x where id_bibxxx = (select id from bib97x where value="%s")'%bibcode)
        if len(ids[0]) == 0:
            print 'bibcode not found in DB'
        elif len(ids[0]) > 1:
            print 'too many ids found for the same bibcode'
        else:
            xml = record_get_xml(ids[0][0])
            print ''.join([l.strip() for l in xml.splitlines()])
    print '</collection>'

def static_file_merging():
    """runs the record merger from a static XML in a file bypassing the extraction"""
    static_file = "misc/2011ApJ...741...91C.xml"
    #static_file = "misc/1999PASP..111..438F.xml"
    #static_file = "misc/1984A&A...130...97L.xml"
    logger.warn(static_file)
    return merge_records_xml(libxml2.parseDoc(open(static_file, "r").read()))


if __name__ == '__main__':
    x = '1999PASP..111..438F'
    merged_record = merge_bibcodes(['2000eaa..bookE1581W', ])
    print merged_record
