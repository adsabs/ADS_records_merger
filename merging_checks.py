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

import logging

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tcpserver')
logger.warning('Protocol problem: %s', 'connection reset')

def check_string_with_unicode_not_selected():
    """Function that checks if a string without unicode has been selected instead of one containing unicode"""
    pass

def check_longer_string_not_selected():
    """"""
    pass

def check_uppercase_string_selected():
    """"""
    pass

def check_no_field_chosen_with_available_fields():
    """"""
    pass

def check_author_from_shorter_list():
    """"""
    pass

def check_pubdate_without_month_selected():
    """It checks if a pubdate without month is selected if other dates with month are present"""
    pass

def check_pubdate_no_match_year_bibcode():
    """"""
    pass

def check_different_pubdates():
    """"""
    pass

def check_different_keywords_for_same_type():
    """"""
    pass

def check_duplicate_normalized_author_names(trusted_author_fields, untrusted_author_fields):
    """
    Checks if there are authors with the same normalized name. This will
    prevent the correct matching of authors from one author list to the other.
    """
    pass
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
