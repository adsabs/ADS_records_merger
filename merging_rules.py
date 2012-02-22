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
from merger_settings import VERBOSE, msg, ORIGIN_SUBFIELD
from merger_errors import OriginValueNotFound
import invenio.bibrecord as bibrecord

class DuplicateNormalizedAuthorError(Exception):
    pass

def priority_based_merger(fields1, record_origin1, fields2, record_origin2, tag, verbose=VERBOSE):
    """basic function that merges based on priority"""
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, record_origin1, fields2, record_origin2, tag)
    except EqualOrigins:
        if len(fields1) == len(fields2) and \
                all(bibrecord._compare_fields(field1, field2, strict=True) for field1, field2 in zip(fields1, fields2)):
            msg('      Equal fields.', verbose)
            return fields1
        else:
            for field1, field2 in zip(fields1, fields2):
                if not bibrecord._compare_fields(field1, field2, strict=False):
                    print tag
                    print fields1, fields2
                    raise
            # Equal fields
            return fields1

    msg('      Selected fields from record %d (%s over %s).' % ( fields1 == trusted and 1 or 2,
        fields1 == trusted and record_origin1 or record_origin2,
        fields1 == trusted and record_origin2 or record_origin1), verbose)
    return trusted

#   else:
#       # In case the two values are identical, return the first one and print
#       # a worning
#       msg('      Same field with origin having the same importance.', verbose)
#       return fields1

def take_all(fields1, record_origin1, fields2, record_origin2, tag, verbose=VERBOSE):
    """function that takes all the different fields
    and returns an unique list"""
    all_fields = []
    for field1 in fields1 + fields2:
        for field2 in all_fields:
            if bibrecord._compare_fields(field1, field2, strict=False):
                break
        else:
            all_fields.append(field1)

    return all_fields

def author_merger(fields1, record_origin1, fields2, record_origin2, tag, verbose=VERBOSE):
    """function that merges the author lists and return the first author or
    all the other authors"""
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, record_origin1, fields2, record_origin2, tag)
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
        author = bibrecord.field_get_subfield_values(field, 'b')[0]
        if author in trusted_authors:
            raise DuplicateNormalizedAuthorError(author)
        else:
            trusted_authors.add(author)

    untrusted_authors = {}
    for field in untrusted:
        author = bibrecord.field_get_subfield_values(field, 'b')[0]
        if author in trusted_authors:
            untrusted_authors[author] = field

    # Now add information from the least trusted list of authors to the most
    # trusted list of authors.
    for index, field in enumerate(trusted):
        author = bibrecord.field_get_subfield_values(field, 'b')[0]
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

def title_merger(fields1, record_origin1, fields2, record_origin2, tag, verbose=VERBOSE):
    """function that chooses the titles and returns the main title or
    the list of alternate titles"""
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, record_origin1, fields2, record_origin2, tag)
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

def abstract_merger(fields1, record_origin1, fields2, record_origin2, tag, verbose=VERBOSE):
    """function that chooses the abstracts based on the languages and priority"""
    try:
        trusted, untrusted = get_trusted_and_untrusted_fields(fields1, record_origin1, fields2, record_origin2, tag)
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

class EqualOrigins(Exception):
    pass

def get_trusted_and_untrusted_fields(fields1, record_origin1, fields2, record_origin2, tag):
    """
    Selects the most trusted fields.
    """
    try:
        origin1 = get_origin_importance(tag, get_origin(fields1))
    except OriginValueNotFound:
        if record_origin1:
            origin1 = record_origin1
            for field in fields1:
                bibrecord.field_add_subfield(field, ORIGIN_SUBFIELD, record_origin1)
        else:
            raise
    try:
        origin2 = get_origin_importance(tag, get_origin(fields2))
    except OriginValueNotFound:
        if record_origin2:
            origin2 = record_origin2
            for field in fields2:
                bibrecord.field_add_subfield(field, ORIGIN_SUBFIELD, record_origin2)
        else:
            print fields2
            raise

    if origin1 > origin2:
        return fields1, fields2
    elif origin1 < origin2:
        return fields2, fields1
    else:
        raise EqualOrigins(get_origin(fields1))
