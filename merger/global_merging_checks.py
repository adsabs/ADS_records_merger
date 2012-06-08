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

Global checks on the entire record.
'''
import logging

from invenio import bibrecord

from merger_settings import FIELD_TO_MARC, \
                    SYSTEM_NUMBER_SUBFIELD, PUBL_DATE_SUBFIELD, \
                    PUBL_DATE_TYPE_SUBFIELD, PUBL_DATE_TYPE_VAL_SUBFIELD,\
                    AUTHOR_NAME_SUBFIELD
from pipeline_log_functions import manage_check_error
import pipeline_settings
logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME)

def check_pub_year_consistency(merged_record, type_check):
    """Function that checks if the publication year is consistent 
    with the year at the beginning of the bibcode"""
    logger.info('      running check_pub_year_consistency')
    #definition of the list of dates I don't want to check with this function
    dates_to_skip_from_check = ['date-preprint']
    try:
        system_number_fields = merged_record[FIELD_TO_MARC['system number']]
    except KeyError:
        manage_check_error('No System Number field!', type_check, logger)
        return None
    try:
        pub_dates_fields = merged_record[FIELD_TO_MARC['publication date']]
    except KeyError:
        manage_check_error('No Publication Date field!', type_check, logger)
        return None
    #the system number field should e unique, so if there are more than 1 fields, I have a problem (and I cannot proceed)
    if len(system_number_fields) > 1:
        manage_check_error('There are more than one System Numbers!', type_check, logger)
        return None
    system_number = bibrecord.field_get_subfield_values(system_number_fields[0], SYSTEM_NUMBER_SUBFIELD)[0]
    num_dates_checked = 0
    for date_type_string in PUBL_DATE_TYPE_VAL_SUBFIELD:
        #I don't want to check the preprint date
        if date_type_string in dates_to_skip_from_check:
            continue
        #then I have to extract the right date (there can be different in the same field)
        pubdate = ''
        for field in pub_dates_fields:
            if bibrecord.field_get_subfield_values(field, PUBL_DATE_TYPE_SUBFIELD)[0] == date_type_string:
                pubdate =  bibrecord.field_get_subfield_values(field, PUBL_DATE_SUBFIELD)[0]
                break
        if len(pubdate) != 0:
            num_dates_checked +=1
        else:
            continue
        #final part of the check
        if pubdate[0:4] != system_number[0:4]:
            manage_check_error('Year of "%s" not consistent with the main bibcode "%s"!' % (date_type_string, system_number), type_check, logger)
    if num_dates_checked == 0:
        manage_check_error('No dates available for this record!', type_check, logger)    
    return None

def first_author_bibcode_consistency(merged_record, type_check):
    """Function that checks if the last letter of the main bibcode 
    is consistent with the first letter of the first author"""
    logger.info('      running first_author_bibcode_consistency')
    bibstems_to_skip_from_check = ['QB']
    try:
        system_number_fields = merged_record[FIELD_TO_MARC['system number']]
    except KeyError:
        manage_check_error('No System Number field!', type_check, logger)
        return None
    try:
        first_author_fields = merged_record[FIELD_TO_MARC['first author']]
    except KeyError:
        manage_check_error('No First Author field!', type_check, logger)
        return None
    #the system number field should e unique, so if there are more than 1 fields, I have a problem (and I cannot proceed)
    if len(system_number_fields) > 1:
        manage_check_error('There are more than one System Numbers!', type_check, logger)
        return None
    #the first author field should e unique, so if there are more than 1 fields, I have a problem (and I cannot proceed)
    if len(first_author_fields) > 1:
        manage_check_error('There are more than one First Author!', type_check, logger)
        return None
    system_number = bibrecord.field_get_subfield_values(system_number_fields[0], SYSTEM_NUMBER_SUBFIELD)[0]
    first_author = bibrecord.field_get_subfield_values(first_author_fields[0], AUTHOR_NAME_SUBFIELD)[0]
    #If the bibcode has a bibstem to skip, I don't do anything
    for elem in bibstems_to_skip_from_check:
        if system_number[4:4+len(elem)] == elem:
            return None
    if first_author[0].lower() != system_number[-1].lower():
        #if the last letter of the system number is a dot, then I want to give a different message
        if system_number[-1] == '.':
            manage_check_error('The main bibcode "%s" doesn\'t have an initial even if there is a First Author "%s"!' % (system_number, first_author), type_check, logger)
        else:
            manage_check_error('First Author "%s" not consistent with the main bibcode "%s"!' % (first_author, system_number), type_check, logger)
    return None

def check_collections_existence(merged_record, type_check):
    """Function that checks if there is at least one collection"""
    logger.info('      running check_collections_existence')
    try:
        collections_fields = merged_record[FIELD_TO_MARC['collection']]
    except KeyError:
        manage_check_error('No Collection field!', type_check, logger)
        return None
    if len(collections_fields) == 0:
        manage_check_error('No Collection field!', type_check, logger)
    return None
    
    