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
The ads merger is a tool that combines two elements and returns
the combined element.
'''
import re

import invenio.bibrecord as bibrecord

from merger_settings import MERGING_RULES, \
                GLOBAL_MERGING_RULES, MARC_TO_FIELD, ORIGIN_SUBFIELD
from pipeline_settings import VERBOSE
from pipeline_log_functions import msg
#from merger_errors import ErrorsInBibrecord, OriginValueNotFound

# Not directly used but needed for evaluation the merging functions.
import merging_rules
import global_merging_rules

def merge_records_xml(marcxml, verbose=VERBOSE):
    """Function that takes in input a marcxml string and returns containing 
    multiple records identified by the tag "collection" and for each calls the 
    function to merge the different flavors of the same record 
    (identified by the tag "record"). """
    #I split the different records Identified by the "collection tag"
    regex = re.compile('<collection>.*?</collection>', re.DOTALL)
    record_xmls = regex.findall(marcxml)
    
    merged_records = []
    for xml in record_xmls:
        records = [res[0] for res in bibrecord.create_records(xml)]
        # Get the merged record.
        merged_records.append(merge_multiple_records(records, verbose))
    return merged_records


def merge_multiple_records(records, verbose=VERBOSE):
    """
    Merges multiple records and returns a merged record.
    """

    if not records:
        return {}
    elif len(records) == 1:
        return merge_two_records(records[0], {}, None, verbose)
    
    record1 = records.pop(0)
    record2 = records.pop(0)
    msg('  Merge #1', verbose)
    
    merged_record = merge_two_records(record1, record2, verbose)
    merge_number = 2
    while records:
        new_record= records.pop(0)
        msg('  Merge #%d' % merge_number, verbose)
        merge_number += 1
        merged_record = merge_two_records(merged_record, new_record, verbose)
    
    #global merging functions
    msg('  Global merging functions', verbose)
    for func in GLOBAL_MERGING_RULES:
        func_to_run = eval(func)
        msg('    Merging with function %s' % func, verbose)
        merged_record = func_to_run(merged_record, verbose)

    record_reorder(merged_record)

    return merged_record

def merge_two_records(record1, record2, verbose=VERBOSE):
    """
    Merges two records and returns a merged record.
    """
    all_tags = sorted(set(record1.keys() + record2.keys()))

    merged_record = {}
    for tag in all_tags:
        fields1 = record1.get(tag, [])
        fields2 = record2.get(tag, [])
        merged_fields = merge_two_fields(tag, fields1, fields2, verbose)
        if merged_fields:
            merged_record[tag] = merged_fields
    
    return merged_record

def merge_two_fields(tag, fields1, fields2, verbose=VERBOSE):
    """
    Merges two sets of fields with the same tag and returns a merged set of
    fields.
    """
    # If one of the two fields does not exist, the merging is trivial.
    merged_fields = []
    msg('    Tag %s:' % tag, verbose)
    merging_func = eval(MERGING_RULES[MARC_TO_FIELD[tag]])
    msg('      Merging with function %s.' % (MERGING_RULES[MARC_TO_FIELD[tag]], ), verbose)
    return merging_func(fields1, fields2, tag, verbose)

def record_reorder(record):
    """
    Resets the field positions to default order of increasing tags. Note that
    the subfield order is kept untouched.
    """
    current_position = 1
    for tag in sorted(record.keys()):
        for index, field in enumerate(record[tag]):
            record[tag][index] = (field[0], field[1], field[2], field[3], current_position)
            current_position += 1

