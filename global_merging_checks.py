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
from invenio import bibrecord

from merger_settings import VERBOSE, msg, manage_check_error, FIELD_TO_MARC, \
                    SYSTEM_NUMBER_SUBFIELD, PUBL_DATE_SUBFIELD, \
                    PUBL_DATE_TYPE_SUBFIELD, PUBL_DATE_TYPE_VAL_SUBFIELD


def check_pub_year_consistency(merged_record, type_check, verbose=VERBOSE):
    """Function that checks if the publication year is consistent 
    with the year at the beginning of the bibcode"""
    msg('      running check_pub_year_consistency', verbose)
    try:
        system_number_fields = merged_record[FIELD_TO_MARC['system number']]
    except KeyError:
        manage_check_error('No System Number field!', type_check)
        return None
    try:
        pub_dates_fields = merged_record[FIELD_TO_MARC['publication date']]
    except KeyError:
        manage_check_error('No Publication Date field!', type_check)
        return None
    #the system number field should e unique, so if there are more than 1 fields, I have a problem (and I cannot proceed)
    if len(system_number_fields) > 1:
        manage_check_error('There are more than one System Numbers!', type_check)
        return None
    system_number = bibrecord.field_get_subfield_values(system_number_fields[0], SYSTEM_NUMBER_SUBFIELD)[0]
    #then I have to extract the right date (there can be different in the same field)
    pubdate = ''
    for field in pub_dates_fields:
        if bibrecord.field_get_subfield_values(field, PUBL_DATE_TYPE_SUBFIELD)[0] == PUBL_DATE_TYPE_VAL_SUBFIELD:
            pubdate =  bibrecord.field_get_subfield_values(field, PUBL_DATE_SUBFIELD)[0]
            break
    if len(pubdate) == 0:
        manage_check_error('No publication date available!', type_check)
        return None
    #final part of the check
    if pubdate[0:4] != system_number[0:4]:
        manage_check_error('Publication year not consistent with the main bibcode!', type_check)
    return None