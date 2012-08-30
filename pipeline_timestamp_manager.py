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

"""
Pipeline timestamp manager.

This module is responsible for comparing the records in ADS and the records in
Invenio. Its only public method is get_record_status() which returns 3 sets of
bibcodes:
    * the bibcodes not yet added to Invenio.
    * the bibcodes of the records that have been modified.
    * the bibcodes of the records that have been deleted in ADS.
"""
import inspect
import ads

from invenio.dbquery import run_sql

from pipeline_settings import BIBCODES_AST, BIBCODES_PHY, BIBCODES_GEN, BIBCODES_PRE, LOGGING_GLOBAL_NAME
#I get the global logger
import logging
logger = logging.getLogger(LOGGING_GLOBAL_NAME)

# Timestamps ordered by increasing order of importance.
TIMESTAMP_FILES_HIERARCHY = [
        BIBCODES_GEN,
        BIBCODES_PRE,
        BIBCODES_PHY,
        BIBCODES_AST,
        ]

def get_records_status():
    """
    Return 3 sets of bibcodes:
    * bibcodes added are bibcodes that are in ADS and not in Invenio.
    * bibcodes modified are bibcodes that are both in ADS and in Invenio and
      that have been modified since the last update.
    * bibcodes deleted are bibcodes that are in Invenio but not in ADS.
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    records_added = []
    records_modified = []
    records_deleted = []

    logger.info('Getting ADS timestamps.')
    ads_timestamps = _get_ads_timestamps()
    logger.info('Getting ADS bibcodes.')
    ads_bibcodes = set(ads_timestamps.keys())
    logger.info('Getting Invenio timestamps.')
    invenio_timestamps = _get_invenio_timestamps()
    logger.info('Getting Invenio bibcodes.')
    invenio_bibcodes = set(invenio_timestamps.keys())

    logger.info('Deducting the added records.')
    records_added = ads_bibcodes - invenio_bibcodes
    logger.info('    %d records to add.' % len(records_added))
    logger.info('Deducting the deleted records.')
    records_deleted = invenio_bibcodes - ads_bibcodes
    logger.info('    %d records to delete.' % len(records_deleted))

    records_to_check = invenio_bibcodes - records_deleted
    logger.info('Checking timestamps for %d records.' % len(records_to_check))

    for bibcode in records_to_check:
        # ADS timestamp in the file has tabs as separators where the XML has
        # colons.
        ads_timestamp = ads_timestamps[bibcode]
        invenio_timestamp = invenio_timestamps[bibcode]

        if invenio_timestamp != ads_timestamp:
            records_modified.append(bibcode)

    logger.info('    %d records to modify.' % len(records_modified))
    logger.info('Done with timestamps.')

    return records_added, records_modified, records_deleted

def _get_invenio_timestamps():
    """
    Returns a set of timestamps found in Invenio.
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    # First get the list of deleted records, i.e. records which have DELETED in 980__c.
    query = "SELECT bb.id_bibrec FROM bib98x AS b, bibrec_bib98x AS bb " \
            "WHERE b.tag='980__c' AND b.value='DELETED' AND b.id=bb.id_bibxxx"
    deleted_recids = set(line[0] for line in run_sql(query))

    # Get the correspondence between recid and bibcode.
    query = "SELECT bb.id_bibrec, b.value FROM bibrec_bib97x AS bb, bib97x AS b " \
            "WHERE bb.id_bibxxx=b.id AND b.tag='970__a'"
    recid_bibcode = dict(run_sql(query))

    # Now get the timestamps.
    query = "SELECT bb.id_bibrec, b.value FROM bibrec_bib99x AS bb, bib99x AS b " \
            "WHERE bb.id_bibxxx=b.id AND b.tag='995__a'"
    timestamps = {}
    for recid, timestamp in run_sql(query):
        if recid not in deleted_recids:
            bibcode = recid_bibcode.get(recid)
            if bibcode is None:
                print 'ERROR: Record %d has no bibcode.' % recid
            else:
                timestamps[bibcode] = timestamp

    return timestamps

def _get_ads_timestamps():
    """
    Merges the timestamp files according to the importance of the database
    in ADS.

    Returns a dictionary with the bibcodes as keys and the timestamps as values.
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    timestamps = {}
    for filename in TIMESTAMP_FILES_HIERARCHY:
        logger.info("Reading \"%s\"" % filename)
        db_timestamps = _read_timestamp_file(filename)
        timestamps.update(db_timestamps)

    # Now let's remove the timestamps of published eprints as they don't appear
    # as such in Invenio.
    published_eprints = [line.strip().split('\t', 1)[1]
                         for line in open(ads.pub2arx)]
    for bibcode in published_eprints:
        try:
            del timestamps[bibcode]
        except:
            pass

    return timestamps

def _read_timestamp_file(filename):
    """
    Reads a timestamp file and returns a dictionary with the bibcodes as keys
    and the timestamps as values.
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    fdesc = open(filename)
    timestamps = {}
    for line in fdesc:
        bibcode, timestamp = line[:-1].split('\t', 1)
        timestamps[bibcode] = timestamp
    fdesc.close()

    return timestamps
