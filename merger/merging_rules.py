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
File containing all the functions to merge
'''

from copy import deepcopy
import logging

import invenio.bibrecord as bibrecord

from basic_functions import get_origin, get_origin_importance, compare_fields_exclude_subfiels
from merger_settings import ORIGIN_SUBFIELD, AUTHOR_NORM_NAME_SUBFIELD,  \
    MARC_TO_FIELD, MERGING_RULES_CHECKS_ERRORS, REFERENCES_MERGING_TAKE_ALL_ORIGINS, \
    REFERENCE_RESOLVED_KEY, REFERENCE_STRING, REFERENCE_EXTENSION,\
    PUBL_DATE_TYPE_VAL_SUBFIELD, PUBL_DATE_SUBFIELD, PUBL_DATE_TYPE_SUBFIELD,\
    CREATION_DATE_TMP_SUBFIELD, MODIFICATION_DATE_TMP_SUBFIELD, PRIMARY_METADATA_SUBFIELD,\
    TEMP_SUBFIELDS_LIST
from merger_errors import GenericError, OriginValueNotFound, EqualOrigins, EqualFields
import pipeline_settings

logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME)

#this import is not explicitly called, but is needed for the import through the settings
import merging_checks

def run_checks(func):
    """Decorator that retrieves and runs the functions 
    to apply to any merging rule"""
    def checks_wrapper(fields1, fields2, tag):
        #I retrieve the groups of functions to run for this field
        try:
            list_checks = MERGING_RULES_CHECKS_ERRORS[MARC_TO_FIELD[tag]]
        except KeyError:
            #If there are no checks I return directly the result of the wrapped function
            return func(fields1, fields2, tag)
        #then I get the result of the wrapped function
        final_result =  func(fields1, fields2, tag)
        #for each warning and error I pass the final_result and all the parameters to the function
        for type_check, functions_check in list_checks.items():
            for func_ck_str, subfield_list in functions_check.items():
                func_ck = eval(func_ck_str)
                func_ck(fields1, fields2, final_result, type_check, subfield_list, tag)
        return final_result
    return checks_wrapper

@run_checks
def priority_based_merger(fields1, fields2, tag):
    """basic function that merges based on priority"""
    #if one of the two lists is empty, I don't have to do anything
    if len(fields1) == 0 or len(fields2) == 0:
        logger.info('        Only one field for "%s".' % tag)
        return fields1+fields2
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag)
    except EqualOrigins:
        #if they have the same origin I try with another approach
        trusted, untrusted = _get_best_fields(fields1, fields2, tag)
    return trusted

def take_all_no_checks(fields1, fields2, tag):
    """function that takes all the different fields
    and returns an unique list"""
    all_fields = []
    for field1 in fields1 + fields2:
        for field2 in all_fields:
            #I check if the fields are the same without considering the origin
            if compare_fields_exclude_subfiels(field1, field2, strict=False, exclude_subfields=[ORIGIN_SUBFIELD]+TEMP_SUBFIELDS_LIST):
                #then I check if with the origin the subfield are the same
                #if so I already have the value in the list
                if bibrecord._compare_fields(field1, field2, strict=False):
                    break
                #otherwise I have to compare the two fields and take the one with the most trusted origin
                else:
                    try:
                        trusted, untrusted = get_trusted_and_untrusted_fields([field1], [field2], tag)
                    except EqualOrigins:
                        try:
                            trusted, untrusted = _get_best_fields([field1], [field2], tag)
                        except EqualFields:
                            break
                    #if the trusted one is already in the list I don't do anything
                    if trusted[0] == field2:
                        break
                    #otherwise I remove the value in the list and I insert the trusted one
                    else:
                        del(all_fields[all_fields.index(field2)])
                        all_fields.append(field1)
                        break
        else:
            all_fields.append(field1)
    return all_fields

@run_checks
def take_all(fields1, fields2, tag):
    """version of the take_all with decorator for checks"""
    return take_all_no_checks(fields1, fields2, tag)

@run_checks
def pub_date_merger(fields1, fields2, tag):
    """function to merge dates. the peculiarity of this merge is that 
    we need to create a new field based on which date is available"""
    all_dates = take_all_no_checks(fields1, fields2, tag)
    if len(all_dates) > 0:
        for date in all_dates:
            #if there is already a main date and it has been created from the primary bibcode I'm done and I can simply return the  merged list
            if bibrecord.field_get_subfield_values(date, PUBL_DATE_TYPE_SUBFIELD)[0] == 'main-date':
                if bibrecord.field_get_subfield_values(date, PRIMARY_METADATA_SUBFIELD)[0] == 'True':
                    logger.info('        Main date already available: returning the dates.')
                    return all_dates
                #otherwise I need to re-create the main date
                #I remove the main-date because I need to re-create it
                else:
                    logger.info('        Main date available but it has not been generated from the canonical metadata: trying to re-create it...')
                    del(all_dates[all_dates.index(date)])
                    break
                
        #I need to extract the best date available
        main_pub_date = None
        main_pub_date_primary = 'False'
        #first I try to extract it from the canonical metadata
        for date_type in PUBL_DATE_TYPE_VAL_SUBFIELD:
            for date in all_dates:
                if bibrecord.field_get_subfield_values(date, PUBL_DATE_TYPE_SUBFIELD)[0] == date_type and bibrecord.field_get_subfield_values(date, PRIMARY_METADATA_SUBFIELD)[0] == 'True':
                    main_pub_date = bibrecord.field_get_subfield_values(date, PUBL_DATE_SUBFIELD)[0]
                    main_pub_date_primary = 'True'
                    break
        #if I'm not successful I try with a normal metadata
        if main_pub_date == None:
            for date_type in PUBL_DATE_TYPE_VAL_SUBFIELD:
                for date in all_dates:
                    if bibrecord.field_get_subfield_values(date, PUBL_DATE_TYPE_SUBFIELD)[0] == date_type:
                        main_pub_date = bibrecord.field_get_subfield_values(date, PUBL_DATE_SUBFIELD)[0]
                        break
        #if I still don't have a main date it means that I have a date that is not in the list of expected dates
        #so I take the first one 
        #P.S. I should never get a this point
        if main_pub_date == None:
            logger.info('        All the dates available are not recognized as good for a main date: picking the first available')
            main_pub_date = bibrecord.field_get_subfield_values(all_dates[0], PUBL_DATE_SUBFIELD)[0]

        #finally I append the main date to the list of dates
        all_dates.append(([(PUBL_DATE_SUBFIELD, main_pub_date), (PUBL_DATE_TYPE_SUBFIELD, 'main-date'), (ORIGIN_SUBFIELD, 'ADS metadata'), 
                           (PRIMARY_METADATA_SUBFIELD, main_pub_date_primary)],) + all_dates[0][1:])
        return all_dates
    else:
        return all_dates

@run_checks
def author_merger(fields1, fields2, tag):
    """function that merges the author lists and return the first author or
    all the other authors"""
    #if one of the two lists is empty, I don't have to do anything
    if len(fields1) == 0 or len(fields2) == 0:
        logger.info('        Only one field for "%s".' % tag)
        return fields1+fields2
    #I need to copy locally the lists of records because I'm going to modify them
    fields1 = deepcopy(fields1)
    fields2 = deepcopy(fields2)
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag)
    except EqualOrigins:
        #if they have the same origin I try with another approach
        trusted, untrusted = _get_best_fields(fields1, fields2, tag)
        #and since I am in this case the two sets of fields are already too similar to enrich the trusted one
        #so I simply return it
        return trusted

    # Sanity check: we have a problem if we have identical normalized author
    # names in the trusted list or if we have identical author names in the
    # untrusted list that is present in the trusted list of authors.
    trusted_authors = set()
    for field in trusted:
        author = bibrecord.field_get_subfield_values(field, AUTHOR_NORM_NAME_SUBFIELD)[0]
        if author in trusted_authors:
            #I don't raise an error if I have duplicated normalized author names,
            #I simply return the trusted list
            logger.info('      Duplicated normalized author name. Skipping author subfield merging.')
            return trusted
            #raise DuplicateNormalizedAuthorError(author)
        else:
            trusted_authors.add(author)

    #I extract all the authors in the untrusted list in case I need to merge some subfields
    untrusted_authors = {}
    for field in untrusted:
        author = bibrecord.field_get_subfield_values(field, AUTHOR_NORM_NAME_SUBFIELD)[0]
        if author in trusted_authors:
            untrusted_authors[author] = field

    # Now add information from the least trusted list of authors to the most
    # trusted list of authors.
    for index, field in enumerate(trusted):
        author = bibrecord.field_get_subfield_values(field, AUTHOR_NORM_NAME_SUBFIELD)[0]
        if author in untrusted_authors:
            trusted_subfield_codes = bibrecord.field_get_subfield_codes(field)
            untrusted_field = untrusted_authors[author]
            untrusted_subfield_codes = bibrecord.field_get_subfield_codes(untrusted_field)

            trusted_subfields = bibrecord.field_get_subfield_instances(field)
            additional_subfield_codes = set(untrusted_subfield_codes) - set(trusted_subfield_codes)
            for code in additional_subfield_codes:
                logger.info('      Subfield "%s" to add to author "%s".' % (code, author))
                additional_subfields = bibrecord.field_get_subfield_values(untrusted_field, code)
                for additional_subfield in additional_subfields:
                    trusted_subfields.append((code, additional_subfield))
            else:
                # Replace the subfields with the new subfields.
                field = (trusted_subfields, field[1], field[2], field[3], field[4])

    return trusted

@run_checks
def title_merger(fields1, fields2, tag):
    """function that chooses the titles and returns the main title or
    the list of alternate titles"""
    #if one of the two lists is empty, I don't have to do anything
    if len(fields1) == 0 or len(fields2) == 0:
        logger.info('        Only one field for "%s".' % tag)
        return fields1+fields2
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag)
    except EqualOrigins:
        #if they have the same origin I try with another approach
        trusted, untrusted = _get_best_fields(fields1, fields2, tag)
    return trusted

@run_checks
def abstract_merger(fields1, fields2, tag):
    """function that chooses the abstracts based on the languages and priority"""
    #if one of the two lists is empty, I don't have to do anything
    if len(fields1) == 0 or len(fields2) == 0:
        logger.info('        Only one field for "%s".' % tag)
        return fields1+fields2
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag)
    except EqualOrigins:
        #if they have the same origin I try with another approach
        trusted, untrusted = _get_best_fields(fields1, fields2, tag)
    return trusted

@run_checks
def references_merger(fields1, fields2, tag):
    """Merging function for references"""
    #if one of the two lists is empty, I don't have to do anything
    if len(fields1) == 0 or len(fields2) == 0:
        logger.info('        Only one field for "%s".' % tag)
        return fields1+fields2
    #first I split the references in two groups: the ones that should be merged and the one that have to taken over the others
    ref_by_merging_type_fields1 = {'take_all':[], 'priority':[]}
    ref_by_merging_type_fields2 = {'take_all':[], 'priority':[]}
        
    #I split the fields1
    for field in fields1:
        if bibrecord.field_get_subfield_values(field, ORIGIN_SUBFIELD)[0] in REFERENCES_MERGING_TAKE_ALL_ORIGINS:
            ref_by_merging_type_fields1['take_all'].append(field)
        else:
            ref_by_merging_type_fields1['priority'].append(field)
    #and the fields2 (this in theory should be always of the same origin type)
    for field in fields2:
        if bibrecord.field_get_subfield_values(field, ORIGIN_SUBFIELD)[0] in REFERENCES_MERGING_TAKE_ALL_ORIGINS:
            ref_by_merging_type_fields2['take_all'].append(field)
        else:
            ref_by_merging_type_fields2['priority'].append(field)
    
    global_list = take_all(take_all(ref_by_merging_type_fields1['take_all'], ref_by_merging_type_fields2['take_all'], tag), 
                           priority_based_merger(ref_by_merging_type_fields1['priority'], ref_by_merging_type_fields2['priority'], tag),
                           tag)
    
    #finally I unique the resolved references
    #taking the reference string (and the related extension handler) from the most trusted origin or 
    #from the other if the most trusted origin has an empty reference string
    #or one with only the bibcode
    unique_references_dict = {}
    unresolved_references = []
    for field in global_list:
        fieldcp = deepcopy(field)
        try:
            bibcode_res = bibrecord.field_get_subfield_values(fieldcp, REFERENCE_RESOLVED_KEY)[0]
        except IndexError:
            bibcode_res = None
        if bibcode_res:
            #first record found
            if bibcode_res not in unique_references_dict:
                unique_references_dict[bibcode_res] = fieldcp
            #merging of subfields
            else:
                #I put in local variable the two list of subfields
                inlist = unique_references_dict[bibcode_res][0]
                outlist = fieldcp[0]
                #I create a new dictionary where to merge the results with the subfields of the first list
                new_subfields = {}
                for subfield in inlist:
                    new_subfields[subfield[0]] = subfield[1]
                origin_imp_inlist = get_origin_importance(tag, new_subfields[ORIGIN_SUBFIELD])
                #then I compare these entries with the values from the second list
                #first I retrieve the origin of the second list and its importance
                for subfield in outlist:
                    if subfield[0] == ORIGIN_SUBFIELD:
                        origin_outlist = subfield[1]
                        origin_imp_outlist = get_origin_importance(tag, subfield[1])
                        break
                #and I retrieve the reference extension if it exists
                extension_outlist = None
                for subfield in outlist:
                    if subfield[0] == REFERENCE_EXTENSION:
                        extension_outlist = subfield[1]
                        break
                #then I merge
                for subfield in outlist:
                    #if I don't have a subfield at all I insert it unless it is a Extension field
                    if subfield[0] not in new_subfields and subfield[0] != REFERENCE_EXTENSION:
                        logger.info('      Subfield "%s" added to reference "%s".' % (subfield[0], bibcode_res))
                        new_subfields[subfield[0]] = subfield[1]
                    #otherwise if it is a reference string
                    elif subfield[0] in new_subfields and subfield[0] == REFERENCE_STRING:
                        #I extract both reference strings
                        refstring_out = subfield[1]
                        refstring_in = new_subfields[REFERENCE_STRING]
                        #if the one already in the list is the bibcode and the other one not I take the other one and I set the origin to the most trusted one
                        if (refstring_in == bibcode_res or len(refstring_in) == 0) and len(refstring_out) != 0:
                            new_subfields[REFERENCE_STRING] = refstring_out
                            logger.info('      Reference string (bibcode only or empty) replaced by the one with origin "%s" for reference %s".' % (origin_outlist, bibcode_res))
                            #if there was an extension for this string I copy also that one
                            if extension_outlist != None:
                                new_subfields[REFERENCE_EXTENSION] = extension_outlist
                                logger.info('      Reference extension replaced by the one with value "%s" for reference %s".' % (extension_outlist, bibcode_res))
                            #I update the origin if the new one is better
                            if origin_imp_outlist > origin_imp_inlist:
                                #first I print the message because I need the old origin
                                logger.info('      Reference origin "%s" replaced by the more trusted "%s".' % (new_subfields[ORIGIN_SUBFIELD], origin_outlist))
                                #then I replace it
                                new_subfields[ORIGIN_SUBFIELD] = origin_outlist
                                
                        #otherwise if the string already in is not a bibcode or empty I have to check the importance
                        else:
                            if origin_imp_outlist > origin_imp_inlist:
                                new_subfields[REFERENCE_STRING] = refstring_out
                                logger.info('      Reference string replaced by the one with origin "%s" for reference %s".' % (origin_outlist, bibcode_res))
                                if extension_outlist != None:
                                    new_subfields[REFERENCE_EXTENSION] = extension_outlist
                                    logger.info('      Reference extension replaced by the one with value "%s" for reference %s".' % (extension_outlist, bibcode_res))
                                #first I print the message because I need the old origin
                                logger.info('      Reference origin "%s" replaced by the more trusted "%s".' % (new_subfields[ORIGIN_SUBFIELD], origin_outlist))
                                new_subfields[ORIGIN_SUBFIELD] = origin_outlist
                    
                #finally I replace the global field
                newrecord = (new_subfields.items(), ) + unique_references_dict[bibcode_res][1:]
                unique_references_dict[bibcode_res] = newrecord
        else:
            unresolved_references.append(fieldcp)
    #and I return the union of the two lists of resolved and unresolved references
    return unique_references_dict.values() + unresolved_references
    

def get_trusted_and_untrusted_fields(fields1, fields2, tag):
    """
    Selects the most trusted fields.
    """
    try:
        origin1 = get_origin(fields1)
        origin_val1 = get_origin_importance(tag, origin1)
    except OriginValueNotFound, error:
        logger.critical(error)
        raise
    try:
        origin2 = get_origin(fields2)
        origin_val2 = get_origin_importance(tag, origin2)
    except OriginValueNotFound, error:
        logger.critical(error)
        raise

    if origin_val1 > origin_val2:
        logger.info('      Selected fields from record 1 (%s over %s).' % (origin1, origin2))
        return fields1, fields2
    elif origin_val1 < origin_val2:
        logger.info('      Selected fields from record 2 (%s over %s).' % (origin2, origin1))
        return fields2, fields1
    else:
        raise EqualOrigins(str(origin1) + ' - ' + str(origin2))
    

def _get_best_fields(fields1, fields2, tag):
    """
    Function that should be called ONLY if "get_trusted_and_untrusted_fields" raises an "EqualOrigins" exception.
    If so this function decides the most trusted based on the actual content of the two sets of fields
    """
    #first check: are the two set of fields exactly the same? if so I take the first one
    if len(fields1) == len(fields2) and all(bibrecord._compare_fields(field1, field2, strict=True) for field1, field2 in zip(fields1, fields2)):
        logger.info('      The two set of fields are exactly the same: picking the first one.')
        return (fields1, fields2)
    #second check: are them the same not considering the origin? If so I take the first one
    if len(fields1) == len(fields2) and all(compare_fields_exclude_subfiels(field1, field2, strict=False, exclude_subfields=[ORIGIN_SUBFIELD]+TEMP_SUBFIELDS_LIST) for field1, field2 in zip(fields1, fields2)):
        logger.info('      The two set of fields are the same (origin excluded): picking the first one.')
        return (fields1, fields2)
    #third check: which one has more fields? If there is one I return this one
    if len(fields1) != len(fields2):
        logger.info('      The two set of fields have different length: picking the longest one.')
        return (fields1, fields2) if len(fields1) > len(fields2) else (fields2, fields1)
    #fourth check: which one has more subfields? If there is one I return this one
    subfields1 = subfields2 = 0
    for field in fields1:
        subfields1 += len(field[0])
    for field in fields2:
        subfields2 += len(field[0]) 
    if subfields1 != subfields2:
        logger.info('      The two set of fields have different number of subfields: picking the set with more subfields.')
        return (fields1, fields2) if subfields1 > subfields2 else (fields2, fields1)
    #fifth check: the sum of all the length of all the strings in the subfields
    subfields_strlen1 = subfields_strlen2 = 0
    for field in fields1:
        for subfield in field[0]:
            if subfield[0] not in TEMP_SUBFIELDS_LIST:
                subfields_strlen1 += len(subfield[1])
    for field in fields2:
        for subfield in field[0]:
            if subfield[0] not in TEMP_SUBFIELDS_LIST:
                subfields_strlen2 += len(subfield[1])
    if subfields_strlen1 != subfields_strlen2:
        logger.info('      The two set of fields have subfields with different length: picking the set with longer subfields.')
        return (fields1, fields2) if subfields_strlen1 > subfields_strlen2 else (fields2, fields1)
    #sixth check: if there is one set of field that has the subfield primary = true I take that one
    try:
        #I count the occorrences of fields with primary true or false
        primary_occurrences_field1 = [bibrecord.field_get_subfield_values(field, PRIMARY_METADATA_SUBFIELD)[0] for field in fields1]
        primary_occurrences_field2 = [bibrecord.field_get_subfield_values(field, PRIMARY_METADATA_SUBFIELD)[0] for field in fields2]
        #then I consider primary = true only if the majority of fields is true
        if primary_occurrences_field1.count('True') > primary_occurrences_field1.count('False'):
            primary_field1 = 'True'
        else:
            primary_field1 = 'False'
        if primary_occurrences_field2.count('True') > primary_occurrences_field2.count('False'):
            primary_field2 = 'True'
        else:
            primary_field2 = 'False'
        #if one of the the two has priority true and the other has false I return the one with true
        if primary_field1 == 'True' and primary_field2 == 'False':
            logger.info('      One set of fields has priority set to True: returning this one')
            return (fields1, fields2)
        if primary_field1 == 'False' and primary_field2 == 'True':
            logger.info('      One set of fields has priority set to True: returning this one')
            return (fields2, fields1)
    except IndexError:
        pass
    try:
        #seventh check: which is the newest file?
        all_dates1 = [bibrecord.field_get_subfield_values(field, CREATION_DATE_TMP_SUBFIELD)[0] for field in fields1] + [bibrecord.field_get_subfield_values(field, MODIFICATION_DATE_TMP_SUBFIELD)[0] for field in fields1]
        all_dates2 = [bibrecord.field_get_subfield_values(field, CREATION_DATE_TMP_SUBFIELD)[0] for field in fields2] + [bibrecord.field_get_subfield_values(field, MODIFICATION_DATE_TMP_SUBFIELD)[0] for field in fields2]
        if max(all_dates1) > max(all_dates2):
            logger.info('      One set of fields is coming from a more recent file: returning this one')
            return (fields1, fields2)
        if max(all_dates2) > max(all_dates1):
            logger.info('      One set of fields is coming from a more recent file: returning this one')
            return (fields2, fields1)
    except IndexError:
        pass
    
    #if all checks fail I reached a granularity of problem too small to make a difference, so I simply return the first one.
    logger.warning('      Set of fields too similar to have an automatic choice: choosing the first one.')
    return (fields1, fields2) 
    
    #if all the checks fail the two set of records are too similar for a script
    #raise EqualFields('Sets of fields too similar to have an automatic choice')