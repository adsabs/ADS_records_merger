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
import sys
import logging

from invenio import bibrecord

from merger_settings import MERGING_RULES, \
                GLOBAL_MERGING_RULES, MARC_TO_FIELD, FIELD_TO_MARC, \
                SYSTEM_NUMBER_SUBFIELD, ORIGIN_SUBFIELD
import pipeline_settings
#from merger_errors import ErrorsInBibrecord, OriginValueNotFound

from misclibs.xml_transformer import create_record_from_libxml_obj 


logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME)

# Not directly used but needed for evaluation the merging functions.
import merging_rules
import global_merging_rules

def merge_records_xml(marcxml_obj):
    """Function that takes in input a marcxml string and returns containing 
    multiple records identified by the tag "collection" and for each calls the 
    function to merge the different flavors of the same record 
    (identified by the tag "record"). """
    logger.info(' Merger started.')
    #I get the bibrecord object from libxml2 one
    all_records = create_record_from_libxml_obj(marcxml_obj, logger)
    merged_records = []
    records_with_merging_probl = []
    for records in all_records:
        #I try to get the bibcode of the record I'm merging
        try:
            system_number_fields = records[0][FIELD_TO_MARC['system number']]
            bibcode = bibrecord.field_get_subfield_values(system_number_fields[0], SYSTEM_NUMBER_SUBFIELD)[0]
        except:
            bibcode = 'Unknown'
        logger.warn(' Merging bibcode "%s".' % bibcode)
        # Get the merged record
        try:
            merged_records.append(merge_multiple_records(records))
        except Exception, error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            str_error_to_print = exc_type.__name__ + '\t' + str(error) + ' (Merger error)'
            logger.error(' Impossible to merge the record "%s" \t %s' % (bibcode, str_error_to_print))
            records_with_merging_probl.append((bibcode, str_error_to_print))
    logger.info(' Merger ended... returning results!')
    return merged_records, records_with_merging_probl


def merge_multiple_records(records):
    """
    Merges multiple records and returns a merged record.
    """

    if not records:
        return {}
    elif len(records) == 1:
        return merge_two_records(records[0], {}, None)
    
    record1 = records.pop(0)
    record2 = records.pop(0)
    logger.info('  Merge #1')
    
    merged_record = merge_two_records(record1, record2)
    merge_number = 2
    while records:
        new_record= records.pop(0)
        logger.info('  Merge #%d' % merge_number)
        merge_number += 1
        merged_record = merge_two_records(merged_record, new_record)
    
    #global merging functions
    logger.info('  Global merging functions')
    for func in GLOBAL_MERGING_RULES:
        func_to_run = eval(func)
        logger.info('    Merging with function %s' % func)
        merged_record = func_to_run(merged_record)

    record_reorder(merged_record)

    return merged_record

def merge_two_records(record1, record2):
    """
    Merges two records and returns a merged record.
    """
    all_tags = sorted(set(record1.keys() + record2.keys()))

    merged_record = {}
    for tag in all_tags:
        fields1 = record1.get(tag, [])
        fields2 = record2.get(tag, [])
        merged_fields = merge_two_fields(tag, fields1, fields2)
        if merged_fields:
            merged_record[tag] = merged_fields
    
    return merged_record

def merge_two_fields(tag, fields1, fields2):
    """
    Merges two sets of fields with the same tag and returns a merged set of
    fields.
    """
    ## If one of the two fields does not exist, the merging is trivial.
    #merged_fields = []
    logger.info('    Tag %s:' % tag)
    merging_func = eval(MERGING_RULES[MARC_TO_FIELD[tag]])
    logger.info('      Merging with function %s.' % (MERGING_RULES[MARC_TO_FIELD[tag]], ))
    return merging_func(fields1, fields2, tag)

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

