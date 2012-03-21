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

import sys
sys.path.append('/proj/ads/soft/python/lib/site-packages')
sys.path.append('/proj/adsx/invenio/lib/python')

from ads.ADSExports import ADSRecords
import invenio.bibrecord as bibrecord

from merger import merge_multiple_records

XSLT = 'misc/AdsXML2MarcXML_v2.xsl'


def merge_bibcode(bibcode, verbose=False):
    """
    Returns a merged version of the record identified by bibcode.
    """
    # Extract the record from ADS.
    records = ADSRecords()
    records.addCompleteRecord(bibcode)
    ads_xml_obj = records.export()
    return merge_ads_xml(ads_xml_obj, verbose)

def merge_ads_xml(ads_xml_obj, verbose=False):
    """"""
    # Convert to MarcXML.
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(XSLT))
    xml_object = stylesheet.applyStylesheet(ads_xml_obj, None)

    # Convert to bibrecord.
    # TODO: We need to allow bibrecord to accept libxml2 objects.
    xml = xml_object.serialize(encoding='utf-8')
    records = [res[0] for res in bibrecord.create_records(xml)]

    # Get the merged record.
    merged_record = merge_multiple_records(records, verbose)

    return merged_record

if __name__ == '__main__':
    merged_record = merge_bibcode('1999PASP..111..438F', verbose=True)
    #print bibrecord.record_xml_output(merged_record)
