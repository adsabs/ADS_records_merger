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
It checks the situation of the latest extraction
if the latest extraction is ok or if there is no extraction I run a new complete extraction (that can be full or an update)
if the last extraction failed, I start again where I stopped the last time

if there has to be a new extraction, I create a new folder with the new four files:
1- the bibcodes to parse (new or modification)
2- the bibcodes to parse (delete)
3- the parsed bibcodes
4- the bibcodes that gave problems during the extraction
then I write the bibcodes to extract in the proper file

Finally I lunch the manager with the entire list of bibcodes to extract

'''

import os
import sys
from time import strftime
import inspect
import shutil

sys.path.append('/proj/ads/soft/python/lib/site-packages')
from ads import Looker

import pipeline_settings as settings
import pipeline_ads_record_extractor
from merger.merger_errors import GenericError
import pipeline_timestamp_manager
import pipeline_settings

#I get the global logger
import logging
logger = logging.getLogger(pipeline_settings.LOGGING_GLOBAL_NAME)


#I define some empty variables
DIRNAME = ''
LATEST_EXTR_DIR = ''
MODE = ''

def manage(mode):
    """public function"""
    logger.info("In function %s" % (inspect.stack()[0][3],))
    
    global MODE
    MODE = mode
    
    #If there is a wrong mode, I will raise an exception
    if mode != 'full' and mode != 'update':
        err_msg = 'Wrong parameter: the extraction can be only "full" or "update"'
        logger.critical(err_msg)
        raise GenericError(err_msg)
    #otherwise I proceed
    else:
        #retrieve the list of bibcode to extract and the list of bibcodes to delete
        (bibcodes_to_extract_list, bibcodes_to_delete_list) = retrieve_bibcodes_to_extract()
        #call the extractor manager
        pipeline_ads_record_extractor.extract(bibcodes_to_extract_list, bibcodes_to_delete_list, DIRNAME)
        return

def retrieve_bibcodes_to_extract():
    """method that retrieves the bibcodes that need to be extracted from ADS"""
    logger.info("In function %s" % (inspect.stack()[0][3],))

    #check the status of the last extraction
    status_last_extraction = check_last_extraction()

    if status_last_extraction == 'OK' or status_last_extraction == 'NOTHING FOUND' or status_last_extraction == 'NOT VALID DIRECTORY CONTENT':
        logger.warning("Last extraction was fine: proceeding with a new one")
        #I create directory and files of bibcodes to extract
        global DIRNAME
        DIRNAME = strftime("%Y_%m_%d-%H_%M_%S")
        os.mkdir(os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME), 0755)
        for filetype in settings.BASE_FILES:
            fileobj = open(os.path.join(os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME), settings.BASE_FILES[filetype]),'w')
            fileobj.write('')
            fileobj.close()
        # I write also the file to log the extraction name
        fileobj = open(os.path.join(os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME), settings.EXTRACTION_FILENAME_LOG),'w')
        fileobj.write('')
        fileobj.close()
        del fileobj
        #then I extract the list of bibcodes according to "mode"
        if MODE == 'full':
            #if node == full I have to extrat all the bibcodes
            return extract_full_list_of_bibcodes()
        elif MODE == 'update':
            return extract_update_list_of_bibcodes()
    else:
        logger.warning("Last extraction was not fine: recovering")
        #I retrieve the bibcodes missing from the last extraction
        DIRNAME = LATEST_EXTR_DIR
        return rem_bibs_to_extr_del(os.path.join(settings.BASE_OUTPUT_PATH, LATEST_EXTR_DIR))


def check_last_extraction():
    """method that checks if the last extraction finished properly"""
    logger.info("In function %s" % (inspect.stack()[0][3],))

    #I retrieve the list of entries in the output directory
    list_of_elements = os.listdir(settings.BASE_OUTPUT_PATH)
    #I extract only the directories
    directories = []
    for elem in list_of_elements:
        if os.path.isdir(os.path.join(settings.BASE_OUTPUT_PATH, elem)):
            directories.append(elem)

    #I set a variable for the latest dir of extraction
    global LATEST_EXTR_DIR
    LATEST_EXTR_DIR = ''

    #if I don't have any result I return the proper status
    if len(directories) == 0:
        logger.info("Checked last extraction: status returned NOTHING FOUND")
        return 'NOTHING FOUND'
    else:
        #I sort the directories in desc mode and I take the first one
        directories.sort(reverse=True)
        LATEST_EXTR_DIR = directories[0]

        logger.info("Checking the directory %s" % os.path.join(settings.BASE_OUTPUT_PATH, LATEST_EXTR_DIR))

        #I extract the content of the last extraction
        elements_from_last_extraction = os.listdir(os.path.join(settings.BASE_OUTPUT_PATH, LATEST_EXTR_DIR))

        #then I check if all the mandatory files are there, otherwise
        for name in settings.BASE_FILES:
            if settings.BASE_FILES[name] not in elements_from_last_extraction:
                logger.info("Checked last extraction: status returned NOT VALID DIRECTORY CONTENT")
                return 'NOT VALID DIRECTORY CONTENT'

        #if I pass all this checks the content is basically fine
        #But then I have to check if the lists of bibcodes are consistent: bibcodes extracted + bibcodes with problems = sum(bibcodes to extract)
        logger.info("Checking if the list of bibcodes actually extracted is equal to the one I had to extract")
        bibcodes_still_pending = extr_diff_bibs_from_extraction(os.path.join(settings.BASE_OUTPUT_PATH, LATEST_EXTR_DIR))
        if len(bibcodes_still_pending) == 0:
            logger.info("All the bibcodes from the last extraction have been processed")
        else:
            logger.info("Checked last extraction: status returned LATEST NOT ENDED CORRECTLY")
            return 'LATEST NOT ENDED CORRECTLY'

    #if everything is Ok I return it
    logger.info("Checked last extraction: status returned OK")
    return 'OK'

def extract_full_list_of_bibcodes():
    """ method that extracts the complete list of bibcodes
        it first extracts the list of arxiv bibcodes and then all the others
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))

    #first I extract the list of preprint
    preprint_bibcodes = read_bibcode_file(settings.BIBCODES_PRE)
    #I copy the preprint file, because I need a copy locally
    try:
        shutil.copy(settings.BIBCODES_PRE, os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME, 'PRE_'+os.path.basename(settings.BIBCODES_PRE)))
    except:
        err_msg = 'Impossible to copy a mandatory file from %s to %s' % (settings.BIBCODES_PRE, os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME))
        logger.critical(err_msg)
        raise GenericError(err_msg)
    #then I extract the complete list
    #all_bibcodes = self.read_bibcode_file(settings.BIBCODES_ALL)
    all_bibcodes = get_all_bibcodes()
    not_pre_bibcodes = list(set(all_bibcodes) - set(preprint_bibcodes))
    not_pre_bibcodes.sort()

    #I write these lists bibcodes to the file of bibcodes to extract
    #and in the meanwhile I create the list with first the preprint and then the published
    bibcode_file = open(os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME, settings.BASE_FILES['new']), 'a')
    bibcode_to_extract = []
    #first the preprints because they can be overwritten by the published ones
    preprint_bibcodes.sort()
    for bibcode in preprint_bibcodes:
        bibcode_file.write(bibcode + '\n')
        bibcode_to_extract.append(bibcode)
    #then all the other bibcodes
    not_pre_bibcodes.sort()
    for bibcode in not_pre_bibcodes:
        bibcode_file.write(bibcode + '\n')
        bibcode_to_extract.append(bibcode)
    bibcode_file.close()
    del bibcode
    del bibcode_file

    logger.info("Full list of bibcodes and related file generated")
    #finally I return the full list of bibcodes and an empty list for the bibcodes to delete
    return (bibcode_to_extract, [])

def extract_update_list_of_bibcodes():
    """Method that extracts the list of bibcodes to update"""
    logger.info("In function %s" % (inspect.stack()[0][3],))

    #I estract the bibcodes
    records_added, records_modified, records_deleted = pipeline_timestamp_manager.get_records_status()
    #I merge the add and modif because I have to extract them in any case
    new_mod_bibcodes_to_extract = list(records_added) + list(records_modified)

    #I extract all the preprint only because then I need to do a diff with the others
    all_preprint_bibcodes = read_bibcode_file(settings.BIBCODES_PRE)
    #I copy the preprint file, because I need a copy locally
    try:
        shutil.copy(settings.BIBCODES_PRE, os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME, 'PRE_'+os.path.basename(settings.BIBCODES_PRE)))
    except:
        err_msg = 'Impossible to copy a mandatory file from %s to %s' % (settings.BIBCODES_PRE, os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME))
        logger.critical(err_msg)
        raise GenericError(err_msg)
    #I extract the not preprint first
    not_pre_bibcodes = list(set(new_mod_bibcodes_to_extract) - set(all_preprint_bibcodes))
    #and then I calculate which are the preprint
    preprint_bibcodes = list(set(new_mod_bibcodes_to_extract) - set(not_pre_bibcodes))
    #then if a preprint that I have to extract has been published, I have to extract also the published bibcode
    published_from_preprint = get_published_from_preprint(preprint_bibcodes)

    bibcodes_to_extract = []
    #then I write all these bibcodes to the proper files
    #first the one to extract
    bibcode_file = open(os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME, settings.BASE_FILES['new']), 'a')
    preprint_bibcodes.sort()
    for bibcode in preprint_bibcodes:
        bibcode_file.write(bibcode + '\n')
        bibcodes_to_extract.append(bibcode)
    published_from_preprint.sort()
    for bibcode in published_from_preprint:
        bibcode_file.write(bibcode + '\n')
        bibcodes_to_extract.append(bibcode)
    not_pre_bibcodes.sort()
    for bibcode in not_pre_bibcodes:
        bibcode_file.write(bibcode + '\n')
        bibcodes_to_extract.append(bibcode)
    bibcode_file.close()

    bibcodes_to_delete = list(records_deleted)
    bibcodes_to_delete.sort()

    #then the one to delete
    bibcode_file = open(os.path.join(settings.BASE_OUTPUT_PATH, DIRNAME, settings.BASE_FILES['del']), 'a')
    for bibcode in bibcodes_to_delete:
        bibcode_file.write(bibcode + '\n')
    bibcode_file.close()

    #I return the list of bibcodes to extract and the list of bibcodes to delete
    return (bibcodes_to_extract, bibcodes_to_delete)

def get_published_from_preprint(preprint_bibcodes):
    """method that given a list of preprint bibcodes, returns a list of published ones (if there are)"""
    logger.info("In function %s" % (inspect.stack()[0][3],))
    #I define a Looker object
    lk =  Looker.Looker(settings.ARXIV2PUB) #@UndefinedVariable #I need this comment so that Eclipse removes the error
    #then I extract the bibcodes connected to the arxiv bibcodes
    published_from_preprint = []
    for bibcode in preprint_bibcodes:
        try:
            pub_bib = map(lambda a: a.split('\t')[1], lk.look(bibcode).strip().split('\n'))[0]
            published_from_preprint.append(pub_bib)
        except Exception:
            pass
    return published_from_preprint


def extr_diff_bibs_from_extraction(extraction_dir):
    """method that extracts the list of bibcodes not processed from a directory used for an extraction"""
    logger.info("In function %s" % (inspect.stack()[0][3],))
    #first I extract the list of bibcodes that I had to extract
    bibcodes_to_extract = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['new']))
    #then the ones I had to delete
    bibcodes_to_delete = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['del']))
    #then the ones that had problems during the extraction
    bibcodes_probl = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['prob']))
    #finally the ones that have been extracted correctly
    bibcodes_done = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['done']))
    #then I extract the ones remaining
    bibcodes_remaining = list((set(bibcodes_to_extract).union(set(bibcodes_to_delete))) - (set(bibcodes_probl).union(set(bibcodes_done))))
    return bibcodes_remaining


def rem_bibs_to_extr_del(extraction_dir):
    """method that finds the bibcodes to extract and to delete not processed in an extraction """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    #first I extract the list of bibcodes that I had to extract
    bibcodes_to_extract = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['new']))
    #then the ones I had to delete
    bibcodes_to_delete = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['del']))
    #then the ones that had problems during the extraction
    bibcodes_probl = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['prob']))
    #finally the ones that have been extracted correctly
    bibcodes_done = read_bibcode_file(os.path.join(extraction_dir, settings.BASE_FILES['done']))

    bibcode_processed = list(set(bibcodes_probl).union(set(bibcodes_done)))
    #then I find the ones remaining to extract
    bibcodes_to_extract_remaining = list(set(bibcodes_to_extract) - set(bibcode_processed))
    #then I find the ones remaining to delete
    bibcodes_to_delete_remaining = list(set(bibcodes_to_delete) - set(bibcode_processed))

    #now I want the list of extraction  ordered with first the preprint and then the other bibcodes
    #only if I have something remaining
    if len(bibcodes_to_extract_remaining) > 0:
        #I load the saved preprint file
        bibcodes_preprint =  read_bibcode_file(os.path.join(settings.BASE_OUTPUT_PATH, extraction_dir, 'PRE_'+os.path.basename(settings.BIBCODES_PRE)))
        remaining_preprint = list(set(bibcodes_to_extract_remaining).intersection(set(bibcodes_preprint)))
        remaining_preprint.sort()
        other_remaining = list(set(bibcodes_to_extract_remaining) - set(remaining_preprint))
        other_remaining.sort()
        bibcodes_to_extract_remaining =  remaining_preprint + other_remaining

    return (bibcodes_to_extract_remaining, bibcodes_to_delete_remaining)

def get_all_bibcodes():
    """Method that retrieves the complete list of bibcodes"""
    logger.info("In function %s" % (inspect.stack()[0][3],))
    # Timestamps ordered by increasing order of importance.
    timestamp_files_hierarchy = [settings.BIBCODES_GEN, settings.BIBCODES_PRE, settings.BIBCODES_PHY, settings.BIBCODES_AST ]

    bibcodes = set([])
    for filename in timestamp_files_hierarchy:
        db_bibcodes = read_bibcode_file(filename)
        bibcodes = bibcodes.union(set(db_bibcodes))
    bibcodes_list = list(bibcodes)
    bibcodes_list.sort()
    return bibcodes_list

def read_bibcode_file(bibcode_file_path):
    """ Function that read the list of bibcodes in one file:
        The bibcodes must be at the beginning of a row.
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    logger.info("Reading %s" % bibcode_file_path)
    try:
        bibfile = open(bibcode_file_path, "rU")
    except IOError:
        err_msg = 'Mandatory file not readable. Please check %s \n' % bibcode_file_path
        logger.critical(err_msg)
        raise GenericError(err_msg)

    bibcodes_list = []

    for bibrow in bibfile:
        if bibrow[0] != " ":
            bibrow_elements =  bibrow.split('\t')
            bibcode = bibrow_elements[0].rstrip('\n')
            if bibcode != '':
                bibcodes_list.append(bibcode)

    bibfile.close()
    del bibfile
    #return the list of bibcodes
    return bibcodes_list




