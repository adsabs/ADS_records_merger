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

from merger.merger import merge_records_xml
import pipeline_settings

XSLT = 'misc/AdsXML2MarcXML_v2.xsl'

logging.basicConfig(format=pipeline_settings.LOGGING_FORMAT)
logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME) #I use this name because then I will use the same in the pipeline
logger.setLevel(logging.INFO)
logger.warning('Test for merger')

def merge_bibcodes(bibcodes):
    """
    Returns a merged version of the record identified by bibcode.
    """
    # Extract the record from ADS.
    records = ADSRecords('full', 'XML')
    for bibcode in bibcodes:
        records.addCompleteRecord(bibcode)
    ads_xml_obj = records.export()
    
    # Convert to MarcXML.
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(XSLT))
    xml_object = stylesheet.applyStylesheet(ads_xml_obj, None)
    
    return merge_records_xml(xml_object)

def static_file_merging():
    """runs the record merger from a static XML in a file bypassing the extraction"""
    static_file = "misc/2011ApJ...741...91C.xml"
    #static_file = "misc/1999PASP..111..438F.xml"
    #static_file = "misc/1984A&A...130...97L.xml"
    logger.warn(static_file)
    return merge_records_xml(libxml2.parseDoc(open(static_file, "r").read()))


if __name__ == '__main__':
    merged_record = merge_bibcodes(['1999PASP..111..438F'])
    #print bibrecord.record_xml_output(merged_record)
