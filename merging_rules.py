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

from basic_functions import get_origin, get_origin_importance, compare_fields_exclude_subfiels
from merger_settings import VERBOSE, msg, ORIGIN_SUBFIELD, AUTHOR_NORM_NAME_SUBFIELD,  \
    MARC_TO_FIELD, MERGING_RULES_CHECKS_ERRORS, REFERENCES_MERGING_TAKE_ALL_ORIGINS, REFERENCE_RESOLVED_KEY, REFERENCE_STRING
from merger_errors import OriginValueNotFound, EqualOrigins
import invenio.bibrecord as bibrecord
#this import is not explicitly called, but is needed for the import through the settings
import merging_checks

def run_checks(func):
    """Decorator that retrieves and runs the functions 
    to apply to any merging rule"""
    def checks_wrapper(fields1, fields2, tag, verbose):
        #I retrieve the groups of functions to run for this field
        try:
            list_checks = MERGING_RULES_CHECKS_ERRORS[MARC_TO_FIELD[tag]]
        except KeyError:
            #If there are no checks I return directly the result of the wrapped function
            return func(fields1, fields2, tag, verbose)
        #then I get the result of the wrapped function
        final_result =  func(fields1, fields2, tag, verbose)
        #for each warning and error I pass the final_result and all the parameters to the function
        for type_check, functions_check in list_checks.items():
            for func_ck_str, subfield_list in functions_check.items():
                func_ck = eval(func_ck_str)
                func_ck(fields1, fields2, final_result, type_check, subfield_list, verbose)
        return final_result
    return checks_wrapper

@run_checks
def priority_based_merger(fields1, fields2, tag, verbose=VERBOSE):
    """basic function that merges based on priority"""
    #if one of the two lists is empty, I don't have to do anything
    if len(fields1) == 0 or len(fields2) == 0:
        return fields1+fields2
    
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag, verbose)
    except EqualOrigins:
        if len(fields1) == len(fields2) and \
                all(bibrecord._compare_fields(field1, field2, strict=True) for field1, field2 in zip(fields1, fields2)):
            msg('      Equal fields.', verbose)
            return fields1
        else:
            for field1, field2 in zip(fields1, fields2):
                if not bibrecord._compare_fields(field1, field2, strict=False):
                    raise
            # Equal fields
            return fields1

    return trusted

#   else:
#       # In case the two values are identical, return the first one and print
#       # a worning
#       msg('      Same field with origin having the same importance.', verbose)
#       return fields1

@run_checks
def take_all(fields1, fields2, tag, verbose=VERBOSE):
    """function that takes all the different fields
    and returns an unique list"""
    all_fields = []
    for field1 in fields1 + fields2:
        for field2 in all_fields:
            #I check if the fields are the same without considering the origin
            if compare_fields_exclude_subfiels(field1, field2, strict=False, exclude_subfields=[ORIGIN_SUBFIELD]):
                #then I check if with the origin the subfield are the same
                #if so I already have the value in the list
                if bibrecord._compare_fields(field1, field2, strict=False):
                    break
                #otherwise I have to compare the two fields and take the one with the most trusted origin
                else:
                    try:
                        trusted, untrusted = get_trusted_and_untrusted_fields([field1], [field2], tag, verbose)
                    except EqualOrigins:
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
def author_merger(fields1, fields2, tag, verbose=VERBOSE):
    """function that merges the author lists and return the first author or
    all the other authors"""
    #I need to copy locally the lists of records because I'm going to modify them
    fields1 = deepcopy(fields1)
    fields2 = deepcopy(fields2)
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag, verbose)
    except EqualOrigins:
        if len(fields1) != len(fields2):
            raise
        else:
            for field1, field2 in zip(fields1, fields2):
                if not bibrecord._compare_fields(field1, field2, strict=False):
                    raise
            # Equal fields
            return fields1

    # Sanity check: we have a problem if we have identical normalized author
    # names in the trusted list or if we have identical author names in the
    # untrusted list that is present in the trusted list of authors.
    trusted_authors = set()
    for field in trusted:
        author = bibrecord.field_get_subfield_values(field, AUTHOR_NORM_NAME_SUBFIELD)[0]
        if author in trusted_authors:
            #I don't raise an error if I have duplicated normalized author names,
            #I simply return the trusted list
            msg('      Duplicated normalized author name. Skipping author subfield merging.', verbose)
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
                msg('      Subfield "%s" to add to author "%s".' % (code, author), verbose)
                additional_subfields = bibrecord.field_get_subfield_values(untrusted_field, code)
                for additional_subfield in additional_subfields:
                    trusted_subfields.append((code, additional_subfield))
            else:
                # Replace the subfields with the new subfields.
                field = (trusted_subfields, field[1], field[2], field[3], field[4])

    return trusted

@run_checks
def title_merger(fields1, fields2, tag, verbose=VERBOSE):
    """function that chooses the titles and returns the main title or
    the list of alternate titles"""
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag, verbose)
    except EqualOrigins:
        if len(fields1) != len(fields2):
            raise
        else:
            for field1, field2 in zip(fields1, fields2):
                if not bibrecord._compare_fields(field1, field2, strict=False):
                    raise
            # Equal fields
            return fields1

    return trusted

@run_checks
def abstract_merger(fields1, fields2, tag, verbose=VERBOSE):
    """function that chooses the abstracts based on the languages and priority"""
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, fields2, tag, verbose)
    except EqualOrigins:
        if len(fields1) != len(fields2):
            raise
        else:
            for field1, field2 in zip(fields1, fields2):
                if not bibrecord._compare_fields(field1, field2, strict=False):
                    raise
            # Equal fields
            return fields1

    return trusted

@run_checks
def references_merger(fields1, fields2, tag, verbose=VERBOSE):
    """Merging function for references"""
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
    
    global_list = take_all(take_all(ref_by_merging_type_fields1['take_all'], ref_by_merging_type_fields2['take_all'], tag, verbose), 
                           priority_based_merger(ref_by_merging_type_fields1['priority'], ref_by_merging_type_fields2['priority'], tag, verbose),
                           tag, verbose)
    
    #finally I unique the resolved references
    #taking the reference string from the most trusted origin or 
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
                #I puth in local variable the two list of subfields
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
                #then I merge
                for subfield in outlist:
                    #if I don't have a subfield at all I insert it
                    if subfield[0] not in new_subfields:
                        msg('      Subfield "%s" added to reference "%s".' % (subfield[0], bibcode_res), verbose)
                        new_subfields[subfield[0]] = subfield[1]
                    #otherwise if it is a reference string
                    elif subfield[0] in new_subfields and subfield[0] == REFERENCE_STRING:
                        #I extract both reference strings
                        refstring_out = subfield[1]
                        refstring_in = new_subfields[REFERENCE_STRING]
                        #if the one already in the list is the bibcode and the other one not I take the other one and I set the origin to the most trusted one
                        if (refstring_in == bibcode_res or len(refstring_in) == 0) and len(refstring_out) != 0:
                            new_subfields[REFERENCE_STRING] = refstring_out
                            msg('      Reference string (bibcode only or empty) replaced by the one with origin "%s for reference %s".' % (origin_outlist, bibcode_res), verbose)
                            #I update the origin if the new one is better
                            if origin_imp_outlist > origin_imp_inlist:
                                #first I print the message because I need the old origin
                                msg('      Reference origin "%s" replaced by the more trusted "%s".' % (new_subfields[ORIGIN_SUBFIELD], origin_outlist), verbose)
                                #then I replace it
                                new_subfields[ORIGIN_SUBFIELD] = origin_outlist
                                
                        #otherwise if the string already in is not a bibcode or empty I have to check the importance
                        else:
                            if origin_imp_outlist > origin_imp_inlist:
                                new_subfields[REFERENCE_STRING] = refstring_out
                                msg('      Reference string replaced by the one with origin "%s for reference %s".' % (origin_outlist, bibcode_res), verbose)
                                #first I print the message because I need the old origin
                                msg('      Reference origin "%s" replaced by the more trusted "%s".' % (new_subfields[ORIGIN_SUBFIELD], origin_outlist), verbose)
                                new_subfields[ORIGIN_SUBFIELD] = origin_outlist
                    
                #finally I replace the global field
                newrecord = (new_subfields.items(), ) + unique_references_dict[bibcode_res][1:]
                unique_references_dict[bibcode_res] = newrecord
        else:
            unresolved_references.append(fieldcp)
    #and I return the union of the two lists of resolved and unresolved references
    return unique_references_dict.values() + unresolved_references
    

def get_trusted_and_untrusted_fields(fields1, fields2, tag, verbose=VERBOSE):
    """
    Selects the most trusted fields.
    """
    try:
        origin1 = get_origin(fields1)
        origin_val1 = get_origin_importance(tag, origin1)
    except OriginValueNotFound:
        raise
    try:
        origin2 = get_origin(fields2)
        origin_val2 = get_origin_importance(tag, origin2)
    except OriginValueNotFound:
        raise

    if origin_val1 > origin_val2:
        msg('      Selected fields from record 1 (%s over %s).' % (origin1, origin2), verbose)
        return fields1, fields2
    elif origin_val1 < origin_val2:
        msg('      Selected fields from record 2 (%s over %s).' % (origin2, origin1), verbose)
        return fields2, fields1
    else:
        raise EqualOrigins(origin1)
