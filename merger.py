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
The ads merger is a tool that combines two elements and returns
the combined element.
'''

import libxslt
import libxml2

import invenio.bibrecord as bibrecord

from ads.ADSExports import ADSRecords

from merger_settings import msg, MERGING_RULES, MARC_TO_FIELD, ORIGIN_SUBFIELD
#from merger_errors import ErrorsInBibrecord, OriginValueNotFound
# Not directly used but needed for evaluation the merging functions.
import merging_rules

XSLT = 'misc/AdsXML2MarcXML_v2.xsl'

def get_ads_xml_from_bibcode(bibcode):
    # Extract the record from ADS.
    records = ADSRecords()
    records.addCompleteRecord(bibcode)
    ads_xml = records.export()
    return ads_xml

def get_bibrecord_from_bibcode(bibcode):
    # Extract the record from ADS.
    records = ADSRecords()
    records.addCompleteRecord(bibcode)
    ads_xml = records.export()

    # Convert to MarcXML.
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(XSLT))
    xml_object = stylesheet.applyStylesheet(ads_xml, None)

    # Convert to bibrecord.
    # TODO: We need to allow bibrecord to accept libxml2 objects.
    xml = xml_object.serialize(encoding='utf-8')
    records = [res[0] for res in bibrecord.create_records(xml)]
    return records

def merge_bibcode(bibcode, verbose=False):
    """
    Returns a merged version of the record identified by bibcode.
    """
    # Extract the record from ADS.
    records = ADSRecords()
    records.addCompleteRecord(bibcode)
    ads_xml = records.export()
    return merge_ads_xml(ads_xml, verbose)

def merge_ads_xml(ads_xml, verbose=False):
    origins = [metadata.prop('origin')
               for metadata in ads_xml.xpathEval('/records/record/metadata')]

    # Convert to MarcXML.
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(XSLT))
    xml_object = stylesheet.applyStylesheet(ads_xml, None)

    # Convert to bibrecord.
    # TODO: We need to allow bibrecord to accept libxml2 objects.
    xml = xml_object.serialize(encoding='utf-8')
    records = [res[0] for res in bibrecord.create_records(xml)]

    # Get the merged record.
    merged_record = merge_multiple_records(records, origins, verbose)

    return merged_record

def merge_multiple_records(records, origins, verbose=False):
    """
    Merges multiple records and returns a merged record.
    """
    if records and not origins:
        origins = [None] * len(records)

    if not records:
        return {}
    elif len(records) == 1:
        return merge_two_records(records[0], origins[0], {}, None, verbose)

    records_origins = zip(records, origins)

    record1, origin1 = records_origins.pop(0)
    record2, origin2 = records_origins.pop(0)
    msg('  Merge #1: Origin1 %s, Origin2 %s' % (origin1 or 'None', origin2 or 'None'), verbose)
    merged_record = merge_two_records(record1, origin1, record2, origin2,
            verbose)
    merge_number = 2
    while records_origins:
        new_record, new_origin = records_origins.pop(0)
        msg('  Merge #%d: Origin2 %s' % (merge_number, new_origin or 'None'), verbose)
        merge_number += 1
        merged_record = merge_two_records(merged_record, None, new_record,
                new_origin, verbose)

    record_reorder(merged_record)

    return merged_record

def merge_two_records(record1, origin1, record2, origin2, verbose=False):
    """
    Merges two records and returns a merged record.
    """
    all_tags = sorted(set(record1.keys() + record2.keys()))

    merged_record = {}
    for tag in all_tags:
        if tag == '961':
            # TODO Do we need to merge creation and modification date?
            continue
        fields1 = record1.get(tag, [])
        fields2 = record2.get(tag, [])
        merged_fields = merge_two_fields(tag, fields1, origin1, fields2,
                    origin2, verbose)
        if merged_fields:
            merged_record[tag] = merged_fields

    return merged_record

def merge_two_fields(tag, fields1, record_origin1, fields2, record_origin2,
        verbose=False):
    """
    Merges two sets of fields with the same tag and returns a merged set of
    fields.
    """
    # First make sure that we have the origin for each field.
    set_origin(fields1, record_origin1)
    set_origin(fields2, record_origin2)

    # If one of the two fields does not exist, the merging is trivial.
    merged_fields = []
    if not fields1:
        msg('    Adding tag %s.' % tag, verbose)
        return fields2
    elif not fields2:
        return fields1

    merging_func = eval(MERGING_RULES[MARC_TO_FIELD[tag]])
    msg('    Tag %s: Merging with function %s.' % (tag, merging_func.func_name), verbose)
    return merging_func(fields1, record_origin1, fields2, record_origin2, tag, verbose)

def record_reorder(record):
    """
    Resets the field positions to default order of increasing tags. Note that
    the subfield order is kept untouched.
    """
    current_position = 1
    for tag in sorted(record.keys()):
        for index, field in enumerate(record[tag]):
            record[tag][index] = (field[0], field[1], field[2], field[3], current_position)
            current_position += 1

def set_origin(fields, origin, force=False):
    """
    Ensures that all the fields in the list are properly tagged with the origin.

    If @force is True, then the origin will be added no matter what, else the
    origin will be added only if there is no other origin.
    """
    if not origin:
        return

    for field in fields:
        origins = bibrecord.field_get_subfield_values(field, ORIGIN_SUBFIELD)
        if (force and origin not in origins) or not origins:
            bibrecord.field_add_subfield(field, ORIGIN_SUBFIELD, origin)

## DEPRECATED ##

#def merge_field(field1, field2, tag, verbose):
#    """Function that merges two fields with a merging function"""
#    # Retrieve the merging function (that is a representation of the merging
#    # rule) for the specified field
#    merging_func = eval(MERGING_RULES[MARC_TO_FIELD[tag]])
#    msg('Merging tag %s with function %s.' % (tag, merging_func.func_name), verbose)
#    return merging_func(field1, field2, tag)

#def merger_field_manager(tag, subfields, verbose):
#    """function that manages the merging of multiple version of a field taking care of combining all the versions"""
#    # Group the subfields per different indicators to merge the subfields inside the different groups
#    grouped_subfields = group_subfields_per_indicator(subfields)
#    # For each group merge the subfields in it
#    merged_fields = []
#    for subfield_group in grouped_subfields:
#        cur_subfields = grouped_subfields[subfield_group]
#        # If there is more than one version, merge the different versions
#        if len(cur_subfields) > 1:
#            # Current version of the field initially is the first version of the record
#            current_version = cur_subfields[0]
#            # Merge it with all the other versions
#            for subfield in cur_subfields[1:]:
#                current_version = merge_field(current_version, subfield, tag, verbose)
#

#            merged_fields.append(current_version)
#        # If there is only one version of the field, do nothing
#        else:
#            merged_fields.append(cur_subfields[0])
#    return merged_fields

#def group_fields(records):
#    """Function that groups together the fields from different version of record
#    i.e. if there are 2 version of field 100 there will be in the dictionary
#    {'100':[[__version 1__], [__version 2__]]}"""
#    grouped_record = {}
#    for record, origin in records:
#        for tag, fields in record.items():
#            grouped_record.setdefault(tag, []).append((fields, origin))
#    return grouped_record

#def group_subfields_per_indicator(subfields):
#    """Function that groups a bunch of subfield per indicator"""
#    grouped_subfields = {}
#    for subfield, origin in subfields:
#        # Extract the indicators
#        indicator1 = subfield[0][1]
#        if indicator1 == ' ':
#            indicator1 = '_'
#        indicator2 = subfield[0][2]
#        if indicator2 == ' ':
#            indicator2 = '_'
#        grouped_subfields.setdefault(indicator1+indicator2, []).append((subfield, origin))
#    return grouped_subfields

#def merge(bibcode, create_records_output, origins=[], verbose=False):
#    """Main function: takes in input a whole record containing the
#    different flavors of metadata

#    @param create_records_output: the output of bibrecord.create_records()
#    @return: a merged record
#    """
#    if origins and len(origins) != len(create_records_output):
#        raise Exception('%s: The number of origins and records does not match.' % bibcode)

#    # The record is in "bibrecord" format (mix of tuples and dictionaries)
#    # Check if there were errors in the conversion to bibrecord format and extract only the metadata from the tuples
#    records = []
#    for index, (record, error_code, error) in enumerate(create_records_output):
#        if error_code == 0:
#            raise ErrorsInBibrecord(error)
#        elif origins:
#            records.append((record, origins[index]))
#        else:
#            records.append((record, None))

#    msg('Merging %d records.' % len(records), verbose)

#    # If we have only one version, we don't need to merge.
#    if len(records) == 1:
#        return records[0][0]

#    # Otherwise merge the single records
#    # First of all group the data per field
#    grouped_record = group_fields(records)

#    # Pass each field to the function that takes care of merge all the versions together
#    # and append the result to the main metadata container
#    merged_record = {}
#    for tag, field_versions in grouped_record.items():
#        # TODO Why is this a list in a list?
#        merged_record[tag] = merger_field_manager(tag, field_versions, verbose)[0]

#    # Correct the field positions.
#    record_reorder(merged_record)

#    return merged_record

if __name__ == '__main__':
    merged_record = merge_bibcode('1999PASP..111..438F', verbose=True)
    #print bibrecord.record_xml_output(merged_record)
