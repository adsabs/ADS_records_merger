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
File containing all the functions to apply after a merging rule has been applied.
All this functions are necessary to create warnings and errors based on the result of a merge
'''

from merger_settings import VERBOSE, msg, manage_check_error, AUTHOR_NORM_NAME_SUBFIELD, \
    KEYWORD_STRING_SUBFIELD, KEYWORD_ORIGIN_SUBFIELD
from invenio import bibrecord


def check_string_with_unicode_not_selected(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """ Function that checks if a string without unicode has been selected instead of one containing unicode.
        If multiple strings have been selected, then only an unicode one is enough to return false.
    """
    def is_unicode(s):
        try:
            s.decode()
            return False
        except UnicodeDecodeError:
            return True 
    
    msg('        running check_string_with_unicode_not_selected', verbose)
    #I extract the fields selected and the ones not selected
    notsel_field_unicode = 0
    #I extract only the subfields from the final result list of fields
    final_result_fields = [field[0] for field in final_result]
    for field in [field[0] for field in fields1+fields2]:
        #non selected field
        if field not in final_result_fields:
            for subfield in field:
                #if I found an unicode string I increase a counter
                if subfield[0] in subfield_list:
                    if is_unicode(subfield[1]):
                        notsel_field_unicode += 1
        #selected field
        else:
            for subfield in field:
                #if I found an unicode string in the selected field then I return directly false
                if subfield[0] in subfield_list:
                    if is_unicode(subfield[1]):
                        return False
    if notsel_field_unicode > 0:
        manage_check_error('Field "%s" with unicode string not selected (all the selected fields are not unicode)!' % tag, type_check)
    return None

def check_longer_string_not_selected(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """"""
    msg('        running check_longer_string_not_selected', verbose)
    
    cur_max_len = 0
    max_len_field_not_sel = False
    
    #I extract only the subfields from the final result list of fields
    final_result_fields = [field[0] for field in final_result]
    for field in [field[0] for field in fields1+fields2]:
        #non selected field
        if field not in final_result_fields:
            for subfield in field:
                #if I have found a field not selected I check if its length is greater than the one I have already checked
                if subfield[0] in subfield_list:
                    if len(subfield[1]) > cur_max_len:
                        #If so I update the variables
                        cur_max_len = len(subfield[1])
                        max_len_field_not_sel = True
        
        #selected field
        else:
            for subfield in field:
                #if I found an unicode string in the selected field then I return directly false
                if subfield[0] in subfield_list:
                    if len(subfield[1]) > cur_max_len:
                        #If so I update the variables
                        cur_max_len = len(subfield[1])
                        max_len_field_not_sel = False
    if max_len_field_not_sel:
        manage_check_error('Longer field "%s" not selected!' % tag, type_check)  
    return None            

def check_uppercase_string_selected(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """"""
    msg('        running check_uppercase_string_selected', verbose)
    #I extract the fields selected and the ones not selected
    notsel_field_lower = 0
    #I extract only the subfields from the final result list of fields
    final_result_fields = [field[0] for field in final_result]
    for field in [field[0] for field in fields1+fields2]:
        #non selected field
        if field not in final_result_fields:
            for subfield in field:
                #if I found a lower case string I increase a counter
                if subfield[0] in subfield_list:
                    if not subfield[1].isupper():
                        notsel_field_lower += 1
        #selected field
        else:
            for subfield in field:
                #if I found an lower case string in the selected field then I return directly false
                if subfield[0] in subfield_list:
                    if not subfield[1].isupper():
                        return False
    if notsel_field_lower > 0:
        manage_check_error('Upper case string selected instead of a lower case one in field "%s"!' % tag, type_check)
    return None

#deprecated: the merging rules always return fields if available
#def check_no_field_chosen_with_available_fields(fields1, fields2, final_result, type_check, subfield_list, verbose=VERBOSE):
#    """"""
#    msg('        check_no_field_chosen_with_available_fields', verbose)
#    
#    return

def check_pubdate_without_month_selected(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """It checks if a pubdate without month is selected if other dates with month are present"""
    msg('        running check_pubdate_without_month_selected', verbose)
    
    #dates in format "YYYY-MM-DD"
    def has_valid_month(date_str):
        try:
            month = int(date_str[5:7])
            return month != 0
        except:
            return False
    
    field_with_month = 0
    #I extract only the subfields from the final result list of fields
    final_result_fields = [field[0] for field in final_result]
    for field in [field[0] for field in fields1+fields2]:
        #non selected field
        if field not in final_result_fields:
            for subfield in field:
                #if I find a date with a valid month I increment the variable
                if subfield[0] in subfield_list:
                    if has_valid_month(subfield[1]):
                        field_with_month += 1
        #selected field
        else:
            for subfield in field:
                #if I find a date with a valid month then I return directly false
                if subfield[0] in subfield_list:
                    if has_valid_month(subfield[1]):
                        return False
    if field_with_month > 0:
        manage_check_error('Date without month selected while other one with month is present in field "%s"!' % tag, type_check)
    return None

#Impossible to implement: it's not possible to have other fields available during merging
#def check_pubdate_no_match_year_bibcode(fields1, fields2, final_result, type_check, subfield_list, verbose=VERBOSE):
#    """"""
#    msg('        running check_pubdate_no_match_year_bibcode', verbose)
#    
#    return

def check_author_from_shorter_list(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """Simply checks that the return list of authors is the longest possible.
        This check relies on the fact that we don't merge authors from different origins, but we simply add subfields
        for the ones we selected.
    """
    msg('        running check_author_from_shorter_list', verbose)
    
    #I select the longest list    
    longer_list = fields1 if len([field[0] for field in fields1]) >= len([field[0] for field in fields2]) else fields2
    #I check if the one returned is shorter than the longest, I have a problem
    if len([field[0] for field in final_result]) < len([field[0] for field in longer_list]):
        manage_check_error('Longer list of authors not selected in field "%s"!' % tag, type_check)
    return None

#Impossible to implement, since we will have different pubdates
#def check_different_pubdates(fields1, fields2, final_result, type_check, subfield_list, verbose=VERBOSE):
#    """"""
#    msg('        check_different_pubdates', verbose)
#    
#    return

def check_different_keywords_for_same_type(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """"""
    msg('        running check_different_keywords_for_same_type', verbose)
    
    #I build a data structure for the keywords of the first set
    #where I group the keywords by institution
    kewords_per_institution = {}
    for field in [field[0] for field in fields1]:
        institution = ' '
        keyword_string = ''
        for subfield in field:
            if subfield[0] == KEYWORD_ORIGIN_SUBFIELD:
                institution = subfield[1]
            if subfield[0] == KEYWORD_STRING_SUBFIELD:
                keyword_string = subfield[1]
        kewords_per_institution.setdefault(institution, set()).add(keyword_string)
    #for each keyword of the other set, I check if it already exists if I already have the same system
    #if I have the same system but not the keyword, then I have a problem
    for field in [field[0] for field in fields2]:
        institution = ' '
        keyword_string = ''
        for subfield in field:
            if subfield[0] == KEYWORD_ORIGIN_SUBFIELD:
                institution = subfield[1]
            if subfield[0] == KEYWORD_STRING_SUBFIELD:
                keyword_string = subfield[1]
        if institution in kewords_per_institution:
            #if I have the same institution then I have to have the the keyword already
            if len(kewords_per_institution[institution].intersection(set([keyword_string]))) == 0:
                manage_check_error('Different groups with same keyword system don\'t have the same list of keywords (field "%s")!' % tag, type_check)
                break
        else:
            pass
    
    return None

def check_one_date_per_type(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """Function to check if there are multiple dates of the same type"""
    msg('        running check_one_date_per_type', verbose)
    
    #I extract all the dates grouped by date type
    date_types = {}
    for field in final_result:
        date_types.setdefault(bibrecord.field_get_subfield_values(field, subfield_list[0][1])[0], []).append(bibrecord.field_get_subfield_values(field, subfield_list[0][0])[0])
    #then I check that these dates are unique per type
    for datet in date_types:
        if len(set(date_types[datet])) > 1:
            manage_check_error('Multiple dates for type "%s" in field "%s".' % (datet, tag), type_check)
    return None
    
def check_duplicate_normalized_author_names(fields1, fields2, final_result, type_check, subfield_list, tag, verbose=VERBOSE):
    """
    Checks if there are authors with the same normalized name. This will
    prevent the correct matching of authors from one author list to the other.
    """
    msg('        running check_duplicate_normalized_author_names', verbose)

    author_names = set()
    for field in final_result:
        author = bibrecord.field_get_subfield_values(field, AUTHOR_NORM_NAME_SUBFIELD)[0]
        if author in author_names:
            #I don't raise an error if I have duplicated normalized author names,
            #I simply return the trusted list
            manage_check_error('Duplicated normalized author name for "%s" in field "%s".' % (author, tag), type_check)
        else:
            author_names.add(author)
    return None
#   trusted_authors = set()
#   for field in trusted_author_fields:
#       author = b.field_get_subfield_values(field, 'b')[0]
#       if author in trusted_authors:
#           logging.warning('Duplicate author ')
#       else:
#           trusted_authors.add(author)

#   untrusted_authors = set()
#   for field in untrusted_author_fields:
#       author = b.field_get_subfield_values(field, 'b')[0]
#       if author in trusted_authors:
#           untrusted_authors[author] = field
