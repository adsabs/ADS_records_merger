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

Global normalization functions for the record.
Some mergings cannot be done based only on one single type of fields, 
but they have to based on multiple field type.
The solution is taking all the fields that cannot be merged during 
a simple merging function and normalize the necessary fields.
'''

from copy import deepcopy
from invenio import bibrecord

from merger_settings import msg, VERBOSE, ORIGIN_SUBFIELD, FIELD_TO_MARC, CREATION_DATE_SUBFIELD, \
                        MODIFICATION_DATE_SUBFIELD, GLOBAL_MERGING_CHECKS
from basic_functions import get_origin_importance
import global_merging_checks


def run_global_checks(func):
    """Decorator that retrieves and runs the functions 
    to apply to any merging rule"""
    def checks_wrapper(merged_record, verbose):
        #I get the result of the wrapped function
        final_result =  func(merged_record, verbose)
        if len(GLOBAL_MERGING_CHECKS) == 0:
            return final_result
        #for each warning and error I pass the final_result and all the parameters to the function
        for type_check, func_ck_list in GLOBAL_MERGING_CHECKS.items():
            for func_ck_str in func_ck_list:
                func_ck = eval(func_ck_str)
                func_ck(final_result, type_check, verbose)
        return final_result
    return checks_wrapper

@run_global_checks       
def merge_creation_modification_dates(merged_record, verbose=VERBOSE):
    """Function that grabs all the origins in the merged record 
    and creates a merged version of the creation and modification date 
    based only on the found origins"""
    #I create a local copy to avoid problems
    record = deepcopy(merged_record)
    #I extract all the creation and modification dates
    try:
        creat_mod = record[FIELD_TO_MARC['creation and modification date']]
    except KeyError:
        msg('      No Creation-Modification field available!', True)
        return record
    #then I extract all the origins from all the fields but the creation and modification date
    origins = []
    for field_code in record:
        if field_code != FIELD_TO_MARC['creation and modification date']:
            for field in record[field_code]:
                try:
                    origin = bibrecord.field_get_subfield_values(field, ORIGIN_SUBFIELD)[0]
                    if origin !='':
                        origins.append(origin)
                #if there is origin this is a problem, but I don't have to manage it here
                except IndexError:
                    pass
    #I unique the list
    origins = list(set(origins))        
    #then for each field in creation e modification date I check if it has an origin used in other fields
    #and if so I update creation and modification dates
    new_creation_modification_date = {}
    for field in creat_mod:
        try:
            origin = bibrecord.field_get_subfield_values(field, ORIGIN_SUBFIELD)[0]
        except IndexError:
            origin = ''
        if origin in origins:
            #I have to put or update the creation and modification date
            if len(new_creation_modification_date) == 0:
                #if there is no creation or modification date I simply insert the field
                new_creation_modification_date[CREATION_DATE_SUBFIELD] = bibrecord.field_get_subfield_values(field, CREATION_DATE_SUBFIELD)[0]
                new_creation_modification_date[MODIFICATION_DATE_SUBFIELD] = bibrecord.field_get_subfield_values(field, MODIFICATION_DATE_SUBFIELD)[0]
                new_creation_modification_date[ORIGIN_SUBFIELD] = origin
                new_creation_modification_date['origin_importance'] = get_origin_importance(FIELD_TO_MARC['creation and modification date'], origin)
            else:
                #otherwise I have to check which one is the oldest for creation and newest for modification
                old_creation = new_creation_modification_date[CREATION_DATE_SUBFIELD]
                old_modification = new_creation_modification_date[CREATION_DATE_SUBFIELD]
                new_creation = bibrecord.field_get_subfield_values(field, CREATION_DATE_SUBFIELD)[0]
                new_modification = bibrecord.field_get_subfield_values(field, MODIFICATION_DATE_SUBFIELD)[0]
                
                new_creation_modification_date[CREATION_DATE_SUBFIELD] = old_creation if old_creation <= new_creation else new_creation
                new_creation_modification_date[CREATION_DATE_SUBFIELD] = old_modification if old_modification >= new_modification else new_modification
                #then at the end I put as origin the most trusted origin
                old_origin = new_creation_modification_date[ORIGIN_SUBFIELD]
                old_origin_import = new_creation_modification_date['origin_importance']
                new_origin_import = get_origin_importance(FIELD_TO_MARC['creation and modification date'], origin)
                new_creation_modification_date[ORIGIN_SUBFIELD] = old_origin if old_origin_import >= new_origin_import else origin
                new_creation_modification_date['origin_importance'] = old_origin_import if old_origin_import >= new_origin_import else new_origin_import
                
    #then I upgrade the field
    record[FIELD_TO_MARC['creation and modification date']] = [([(MODIFICATION_DATE_SUBFIELD, new_creation_modification_date[MODIFICATION_DATE_SUBFIELD]), 
                               (CREATION_DATE_SUBFIELD, new_creation_modification_date[CREATION_DATE_SUBFIELD]),
                               (ORIGIN_SUBFIELD, new_creation_modification_date[ORIGIN_SUBFIELD])], ) + creat_mod[0][1:]]
    return record
    
    
    
    
    
    