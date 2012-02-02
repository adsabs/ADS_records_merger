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

from basic_functions import get_origin, get_origin_importance
from merger_settings import VERBOSE, msg
import invenio.bibrecord as b

def priority_based_merger(fields1, fields2, tag, verbose=VERBOSE):
    """basic function that merges based on priority"""
    origin_val1 = get_origin_importance(tag, get_origin(fields1))
    origin_val2 = get_origin_importance(tag, get_origin(fields2))
    if origin_val1 > origin_val2:
        return fields1
    elif origin_val2 > origin_val1:
        return fields2
    else:
        # In case the two values are identical, return the first one and print
        # a worning
        msg(verbose, 'Same field with origin having the same importance.', verbose)
        return fields1

def take_all(fields1, fields2, tag, verbose=VERBOSE):
    """function that takes all the different fields
    and returns an unique list"""
    all_fields = []
    for field1 in fields1 + fields2:
        for field2 in all_fields:
            if b._compare_fields(field1, field2, strict=False):
                break
        else:
            all_fields.append(field1)

    return all_fields

def author_merger(fields1, fields2, tag, verbose=VERBOSE):
    """function that merges the author lists and return the first author or
    all the other authors"""

    trusted, untrusted = None, None

    # First select the most trusted author list.
    origin_val1 = get_origin_importance(tag, get_origin(fields1))
    origin_val2 = get_origin_importance(tag, get_origin(fields2))
    if origin_val1 > origin_val2:
        trusted, untrusted = fields1, fields2
    elif origin_val2 > origin_val1:
        trusted, untrusted = fields2, fields1

    # Create a dictionary of normalized author names for easy searching.
    untrusted_authors = {}
    for field in untrusted:
        author = b.field_get_subfield_values(field, 'b')[0]
        untrusted_authors[author] = field

    # Now add information from the least trusted list of authors to the most
    # trusted list of authors.
    for index, field in enumerate(trusted):
        author = b.field_get_subfield_values(field, 'b')[0]
        if author in untrusted_authors:
            trusted_subfield_codes = b.field_get_subfield_codes(field)
            untrusted_field = untrusted_authors[author]
            untrusted_subfield_codes = b.field_get_subfield_codes(untrusted_field)

            trusted_subfields = b.field_get_subfield_instances(field)
            additional_subfield_codes = set(untrusted_subfield_codes) - set(trusted_subfield_codes)
            for code in additional_subfield_codes:
                msg('Subfield "%s" to add to author "%s".' % (code, author))
                additional_subfields = b.field_get_subfield_values(untrusted_field, code)
                for additional_subfield in additional_subfields:
                    trusted_subfields.append((code, additional_subfield))
            else:
                # Replace the subfields with the new subfields.
                field = (trusted_subfields, field[1], field[2], field[3], field[4])

    return trusted

def title_merger(fields1, fields2, tag, verbose=VERBOSE):
    """function that chooses the titles and returns the main title or
    the list of alternate titles"""
    pass

def abstract_merger(fields1, fields2, tag, verbose=VERBOSE):
    """function that chooses the abstracts based on the languages and priority"""
    pass
