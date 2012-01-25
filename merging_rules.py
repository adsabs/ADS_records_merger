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
@author: Giovanni Di Milia,
File containing all the functions to merge
'''

from basic_functions import get_origin, get_origin_value, printmsg
from merger_settings import VERBOSE
from invenio.bibrecord import _compare_fields

def priority_based_merger(fields1, fields2, field_code, verbose=VERBOSE):
    """basic function that merges based on priority"""

    try:
        origin_val1 = get_origin_value(field_code, get_origin(fields1))
        origin_val2 = get_origin_value(field_code, get_origin(fields2))
    except:
        print fields1
        print fields2
        raise

    if origin_val1 > origin_val2:
        return fields1
    elif origin_val2 > origin_val1:
        return fields2
    else:
        # In case the two values are identical, return the first one and print
        # a worning
        printmsg(verbose, 'Same field with origin having the same importance.')
        return fields1

def take_all(fields1, fields2, field_code):
    """function that takes all the different fields
    and returns an unique list"""
    all_fields = []
    for field1 in fields1 + fields2:
        for field2 in all_fields:
            if _compare_fields(field1, field2, strict=False):
                break
        else:
            all_fields.append(field1)

    return all_fields

def author_merger(fields1, fields2, field_code):
    """function that merges the author lists and return the first author or
     all the other authors"""
    pass

def title_merger(fields1, fields2, field_code):
    """function that chooses the titles and returns the main title or
    the list of alternate titles"""
    pass

def abstract_merger(fields1, fields2, field_code):
    """function that chooses the abstracts based on the languages and priority"""
    pass
