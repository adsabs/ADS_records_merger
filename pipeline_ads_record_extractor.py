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
The manager is the leading process for the extraction
It takes in input a list of bibcodes
then it splits the list in multiple groups sized according to the settings
these groups are put in a "to process queue"
different processes will take a group each from the "to process queue" and they will extract the bibcodes assigned
after the extraction they will insert the processed bibcodes in an unique "processed queue"
finally a last process will take the processed bibcodes and will write them to the proper file
This class uses multiprocessing, so it is compatible only with python 2.6+
'''

import sys
sys.path.append('/proj/ads/soft/python/lib/site-packages')

import inspect
import multiprocessing
import libxml2
import itertools
import os
import pickle

from ads.ADSExports import ADSRecords

from invenio import bibrecord

import pipeline_settings as settings
import pipeline_write_files as write_files
import misclibs.xml_transformer as xml_transformer
from merger.merger_errors import GenericError
from merger import merger
from pipeline_invenio_uploader import bibupload_merger
import pipeline_settings

#I get the global logger
import logging
logger = logging.getLogger(pipeline_settings.LOGGING_GLOBAL_NAME)

#some global variables
BIBCODES_TO_EXTRACT_LIST = []
BIBCODES_TO_DELETE_LIST = []
EXTRACTION_DIRECTORY = ''


def extract(bibcodes_to_extract_list, bibcodes_to_delete_list, file_to_upload_remaining, extraction_directory):
    """manager of the extraction"""
    logger.info("In function %s" % (inspect.stack()[0][3],))
    
    global EXTRACTION_DIRECTORY, BIBCODES_TO_DELETE_LIST, BIBCODES_TO_EXTRACT_LIST
    #the bibcodes to extract MUST NOT be sorted
    BIBCODES_TO_EXTRACT_LIST = bibcodes_to_extract_list
    BIBCODES_TO_DELETE_LIST = bibcodes_to_delete_list
    BIBCODES_TO_DELETE_LIST.sort()
    EXTRACTION_DIRECTORY = extraction_directory
    #I extract or generate the extraction name
    EXTRACTION_NAME = set_extraction_name()
    
    ########################################################################
    #part where the bibcode to delete are processed

    #I have to upload first the bibcodes to delete and then the others.
    #So I process them first
    if BIBCODES_TO_DELETE_LIST:
        try:
            process_bibcodes_to_delete()
        except Exception:
            err_msg = 'Unable to process the bibcodes to delete'
            logger.error(err_msg)
            raise GenericError(err_msg)

    ########################################################################
    #part where the bibcode to extract (new or update) are processed

    #I split the list of bibcodes to process in multiple groups
    bibtoprocess_splitted = grouper(settings.NUMBER_OF_BIBCODES_PER_GROUP, BIBCODES_TO_EXTRACT_LIST)

    #I define a manager for the workers
    manager = multiprocessing.Process(target=extractor_manager_process, args=(bibtoprocess_splitted, file_to_upload_remaining, EXTRACTION_DIRECTORY, EXTRACTION_NAME))
    #I start the process
    manager.start()
    #I join the process
    manager.join()

    #just before the end of the extraction, I write the message that the extraction finished and the files are ready to be uploaded in the extraction log file
    filepath = os.path.join(settings.BASE_OUTPUT_PATH, EXTRACTION_DIRECTORY, settings.EXTRACTION_FILENAME_LOG)
    file_obj = open(filepath,'a')
    file_obj.write(settings.EXTRACTION_READY_TO_UPLOAD_MESSAGE + '\n')
    file_obj.close()

    logger.warning("Extraction ended!")


def grouper(n, iterable):
    """method to split a list in multiple groups"""
    logger.info("In function %s" % (inspect.stack()[0][3],))
    args = [iter(iterable)] * n
    return list(([e for e in t if e != None] for t in itertools.izip_longest(*args)))


def process_bibcodes_to_delete():
    """method that creates the MarcXML for the bibcodes to delete"""
    logger.info("In function %s" % (inspect.stack()[0][3],))

    #I create an unique file for all the bibcodes to delete:
    #I don't think it's necessary to split the content in groups, since the XML is really simple

    #I create the base object for the tree
    doc = libxml2.newDoc("1.0")
    root = doc.newChild(None, "collection", None)

    #then for each bibcode to delete I create the proper record
    for bibcode in BIBCODES_TO_DELETE_LIST:
        record = root.newChild(None, 'record', None)
        #I add to the record the 2 necessary datafields
        d970 = record.newChild(None, 'datafield', None)
        d970.setProp('tag', '970')
        d970.setProp('ind1', '')
        d970.setProp('ind2', '')
        #I create the subfield tag
        sub = d970.newChild(None, 'subfield', bibcode.replace('&', '&amp;'))
        sub.setProp("code", "a")
        d980 = record.newChild(None, 'datafield', None)
        d980.setProp('tag', '980')
        d980.setProp('ind1', '')
        d980.setProp('ind2', '')
        #I create the subfield tag
        sub = d980.newChild(None, 'subfield', "DELETED")
        sub.setProp("code", "c")

    #I extract the node
    marcxml_string = doc.serialize('UTF-8', 1)
    #I remove the data
    doc.freeDoc()
    del doc

    #I transform the xml in bibrecords
    bibrecord_object = bibrecord.create_records(marcxml_string)
    #I upload the result with option append
    bibupload_merger(bibrecord_object, logger, 'append')
    
    return True

def set_extraction_name():
    """Method that sets the name of the current extraction"""
    logger.info("In function %s" % (inspect.stack()[0][3],))

    filepath = os.path.join(settings.BASE_OUTPUT_PATH, EXTRACTION_DIRECTORY, settings.EXTRACTION_FILENAME_LOG)
    file_obj = open(filepath,'r')
    rows = file_obj.readlines()
    file_obj.close()
    if len(rows) > 0:
        #I check the rows starting from the last one until I reach a valid extraction name. I do in this way because I use the log file also for other stuff
        line_range = range(len(rows))
        line_range.sort(reverse=True)
        for i in line_range:
            last_name =  rows[i]
            if last_name.startswith(settings.EXTRACTION_BASE_NAME):
                break
        number_ext = int(last_name.split(settings.EXTRACTION_BASE_NAME)[1])
        number_ext = number_ext + 1
    else:
        last_name = None
        number_ext = 1

    extraction_name = settings.EXTRACTION_BASE_NAME + str(number_ext)
    #Then I write the number of extraction to the file
    file_obj = open(filepath,'a')
    file_obj.write(extraction_name + '\n')
    file_obj.close()

    return extraction_name


def extractor_manager_process(bibtoprocess_splitted, file_to_upload_remaining, extraction_directory, extraction_name):
    """Process that takes care of managing all the other worker processes
        this process also creates new worker processes when the existing ones reach the maximum number of groups of bibcode to process
    """
    logger.info("In function %s" % (inspect.stack()[0][3],))
    #a queue for the bibcodes to process
    q_todo = multiprocessing.Queue()
    #a queue for the bibcodes processed
    q_done = multiprocessing.Queue()
    #a queue for the bibcodes with problems
    q_probl = multiprocessing.Queue()
    #a lock to write in stdout
    lock_stdout = multiprocessing.Lock()
    #a queue for the messages from the workers that have to tell the manager when they reach the maximum number of chunks to process
    q_life = multiprocessing.Queue()
    #a queue to pass the files to upload to the dedicated processes
    q_uplfile = multiprocessing.Queue()
    #a lock for the worker processes to access the log of the done files
    lock_createdfiles = multiprocessing.Lock()
    #a lock for the uploader processes to access the log of the uploaded files
    lock_donefiles = multiprocessing.Lock()

    logger.info(multiprocessing.current_process().name + ' (Manager) Filling the queue with the tasks')

    #I split all the bibcodes in groups of NUMBER_OF_BIBCODES_PER_GROUP and I put them in the todo queue
    counter = 0 #I need the counter to uniquely identify each group
    for grp in bibtoprocess_splitted:
        counter += 1
        q_todo.put([str(counter).zfill(7), grp])
    #I pre-fill the list of files to upload if there are some
    file_to_upload_remaining.sort()
    for file2up in file_to_upload_remaining:
        q_uplfile.put(('Previous Extraction', file2up))

    #I define the number of processes to run
    number_of_processes = settings.NUMBER_WORKERS 
    
    logger.info(multiprocessing.current_process().name + ' (Manager) Creating the output workers')
    #I define a "done bibcode" worker
    donebib = multiprocessing.Process(target=done_extraction_process, args=(q_done, number_of_processes, lock_stdout, q_life, extraction_directory))
    #I define a "problematic bibcode" worker
    problbib = multiprocessing.Process(target=problematic_extraction_process, args=(q_probl, number_of_processes, lock_stdout, q_life, extraction_directory))
    
    logger.info(multiprocessing.current_process().name + ' (Manager) Creating the upload workers')
    upload_processes = [multiprocessing.Process(target=upload_process, args=(q_uplfile, lock_stdout, lock_donefiles, q_life, extraction_directory, extraction_name)) for i in range(settings.NUMBER_UPLOAD_WORKER)]
    
    logger.info(multiprocessing.current_process().name + ' (Manager) Creating the first pool of workers')
    #I define the worker processes
    processes = [multiprocessing.Process(target=extractor_process, args=(q_todo, q_done, q_probl, q_uplfile, lock_stdout, lock_createdfiles, q_life, extraction_directory, extraction_name)) for i in range(number_of_processes)]
    #I append to the todo queue a list of commands to stop the worker processes
    for i in range(number_of_processes):
        q_todo.put(['STOP', ''])


    logger.warning(multiprocessing.current_process().name + ' (Manager) Starting all the workers')
    
    #I start the output handlers
    donebib.start()
    problbib.start()
    #I start the upload processes
    for pu in upload_processes:
        pu.start()
    #I start the worker processes
    for p in processes:
        p.start()
    
    #then I have to wait for the workers that have to tell me if they reached the maximum amount of chunk to process or if the extraction ended
    #in the first case I have to start another process
    #in the second I have to decrease the counter of active workers
    active_workers = settings.NUMBER_WORKERS
    active_upload_workers = settings.NUMBER_UPLOAD_WORKER
    additional_workers = 2
    while active_workers > 0 or additional_workers > 0 or active_upload_workers > 0:
        #I get the message from the worker
        death_reason = q_life.get()
        #if the reason of the death is that the process reached the max number of groups to process, then I have to start another one
        if death_reason[0] == 'MAX LIFE REACHED':
            newprocess = multiprocessing.Process(target=extractor_process, args=(q_todo, q_done, q_probl, q_uplfile, lock_stdout, lock_createdfiles, q_life, extraction_directory, extraction_name))
            newprocess.start()
            #!!!!!!!!!!!!!!!!!!!!!!!!
            #this call is probably wrong: to check
            #additional_workers = additional_workers - 1
            #!!!!!!!!!!!!!!!!!!!!!!!!
            lock_stdout.acquire()
            logger.warning(multiprocessing.current_process().name + ' (Manager) New worker created')
            lock_stdout.release()
        elif death_reason[0] == 'QUEUE EMPTY':
            active_workers = active_workers - 1
            lock_stdout.acquire()
            logger.info(multiprocessing.current_process().name + ' (Manager) %s workers waiting to finish their job' % str(active_workers))
            lock_stdout.release()
            #if there are no more worker processes active, it means that I can tell the uploader that they can exit as soon as the are done
            if active_workers == 0:
                lock_stdout.acquire()
                logger.info(multiprocessing.current_process().name + ' (Manager) Telling the upload workers that the extraction workers are done')
                lock_stdout.release()
                for i in range(settings.NUMBER_UPLOAD_WORKER):
                    q_uplfile.put(['WORKERS DONE'])
        elif death_reason[0] == 'PROBLEMBIBS DONE':
            additional_workers = additional_workers - 1
            lock_stdout.acquire()
            logger.info(multiprocessing.current_process().name + ' (Manager) %s additional workers waiting to finish their job' % str(additional_workers))
            lock_stdout.release()
        elif death_reason[0] == 'DONEBIBS DONE':
            additional_workers = additional_workers - 1
            lock_stdout.acquire()
            logger.info(multiprocessing.current_process().name + ' (Manager) %s additional workers waiting to finish their job' % str(additional_workers))
            lock_stdout.release()
        elif death_reason[0] == 'UPLOAD DONE':
            active_upload_workers = active_upload_workers - 1
            lock_stdout.acquire()
            logger.info(multiprocessing.current_process().name + ' (Manager) %s upload workers waiting to finish their job' % str(active_upload_workers))
            lock_stdout.release()

    lock_stdout.acquire()
    logger.info(multiprocessing.current_process().name + ' (Manager) All the workers are done. Exiting...')
    lock_stdout.release()


def extractor_process(q_todo, q_done, q_probl, q_uplfile, lock_stdout, lock_createdfiles, q_life, extraction_directory, extraction_name):
    """Worker function for the extraction of bibcodes from ADS
        it has been defined outside any class because it's more simple to treat with multiprocessing """
    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (worker) Process started')
    lock_stdout.release()
    #I create a local logger
    fh = logging.FileHandler(os.path.join(pipeline_settings.BASE_OUTPUT_PATH, extraction_directory, pipeline_settings.BASE_LOGGING_PATH, multiprocessing.current_process().name+'_worker.log'))
    fmt = logging.Formatter(pipeline_settings.LOGGING_FORMAT)
    fh.setFormatter(fmt)
    local_logger = logging.getLogger(pipeline_settings.LOGGING_WORKER_NAME)
    local_logger.addHandler(fh)
    local_logger.setLevel(logger.level)
    local_logger.propagate = False
    #I print the same message for the local logger
    local_logger.warning(multiprocessing.current_process().name + ' Process started')
    
    #I get the maximum number of groups I can process
    max_num_groups = settings.MAX_NUMBER_OF_GROUP_TO_PROCESS
    #variable used to know if I'm exiting because the queue is empty or because I reached the maximum number of groups to process
    queue_empty = False

    #while there is something to process or I reach the maximum number of groups I can process,  I try to process
    for grpnum in range(max_num_groups):

        task_todo = q_todo.get()
        if task_todo[0] == 'STOP':

            queue_empty = True
            #I exit the loop
            break

        #I print when I'm starting the extraction
        local_logger.warning(multiprocessing.current_process().name + (' starting to process group %s' % task_todo[0]))

        ############
        #then I process the bibcodes
        # I define a couple of lists where to store the bibcodes processed
        bibcodes_ok = []
        bibcodes_probl = []

        #I define a ADSEXPORT object
        recs = ADSRecords('full', 'XML')

        # I define a maximum amount of bibcodes I can skip per each cicle: the number of bibcodes per group / 10 (minimum 500)
        # if i skip more than this amount it means that there is something
        # wrong with the access to the data and it's better to stop everything
        max_number_of_bibs_to_skip = max(settings.NUMBER_OF_BIBCODES_PER_GROUP / 10, settings.MAX_SKIPPED_BIBCODES)

        for bibcode in task_todo[1]:
            try:
                recs.addCompleteRecord(bibcode)
                bibcodes_ok.append(bibcode)
            except Exception, error:
                local_logger.error(': problem retrieving the bibcode "%s" in group %s' % (bibcode, task_todo[0]))
                #I catch the exception type name
                exc_type, exc_obj, exc_tb = sys.exc_info()
                try:
                    str_error_to_print = exc_type.__name__ + '\t' + str(error)
                except:
                    try:
                        str_error_to_print = u'%s\t%s' % (unicode(exc_type.__name__), unicode(error))
                    except:
                        local_logger.error(' Cannot log error for bibcode %s ' % bibcode)
                        str_error_to_print = ''
                bibcodes_probl.append((bibcode, str_error_to_print))
                max_number_of_bibs_to_skip = max_number_of_bibs_to_skip - 1
            #If i=I reach 0 It means that I skipped 1k bibcodes and probably there is a problem: so I simulate an exit for empty queue
            if max_number_of_bibs_to_skip == 0:
                break
        #I exit from both loops
        if max_number_of_bibs_to_skip == 0:
            lock_stdout.acquire()
            local_logger.warning(multiprocessing.current_process().name + (' Detected possible error with ADS data access: skipped %s bibcodes in one group' % max(settings.NUMBER_OF_BIBCODES_PER_GROUP / 10, settings.MAX_SKIPPED_BIBCODES)))
            lock_stdout.release()
            queue_empty = True
            break

        #I extract the object I created
        xmlobj = recs.export()
        del recs

        try:
            #I define a transformation object
            transf = xml_transformer.XmlTransformer(local_logger)
            #and I transform my object
            marcxml = transf.transform(xmlobj)
        except:
            err_msg = ' Impossible to transform the XML!'
            local_logger.critical(err_msg)
            raise GenericError(err_msg)

        if marcxml:
            #I merge the records
            merged_records, records_with_merging_probl = merger.merge_records_xml(marcxml)
            #If I had problems to merge some records I remove the bibcodes from the list "bibcodes_ok" and I add them to "bibcodes_probl"
            for elem in records_with_merging_probl:
                bibcodes_ok.remove(elem[0])
            bibcodes_probl = bibcodes_probl + records_with_merging_probl
            #########
            #I write the object in a file
            ##########
            filepath = os.path.join(settings.BASE_OUTPUT_PATH, extraction_directory, pipeline_settings.BASE_BIBRECORD_FILES_DIR, pipeline_settings.BIBREC_FILE_BASE_NAME+'_'+extraction_name+'_'+task_todo[0])
            output = open(filepath, 'wb')
            pickle.dump(merged_records, output)
            output.close()
            #then I write the filepath to a file for eventual future recovery
            lock_createdfiles.acquire()
            bibrec_file_obj = open(os.path.join(settings.BASE_OUTPUT_PATH, extraction_directory,settings.LIST_BIBREC_CREATED), 'a')
            bibrec_file_obj.write(filepath + '\n')
            bibrec_file_obj.close()
            lock_createdfiles.release()
            #finally I append the file to the queue
            q_uplfile.put((task_todo[0],filepath))
            
            #logger.info('record created, merged but not uploaded')
            #bibupload_merger(merged_records, local_logger, 'replace_or_insert')
            
            
        #otherwise I put all the bibcodes in the problematic
        else:
            bibcodes_probl = bibcodes_probl + [(bib, 'Bibcode extraction ok, but xml generation failed') for bib in bibcodes_ok]
            bibcodes_ok = []
        
        
        #finally I pass to the done bibcodes to the proper file
        q_done.put([task_todo[0], bibcodes_ok])
        #and the problematic bibcodes
        q_probl.put([task_todo[0], bibcodes_probl])

        local_logger.warning(multiprocessing.current_process().name + (' finished to process group %s' % task_todo[0]))


    if queue_empty:
        #I tell the output processes that I'm done
        q_done.put(['WORKER DONE'])
        q_probl.put(['WORKER DONE'])
        #I tell the manager that I'm dying because the queue is empty
        q_life.put(['QUEUE EMPTY'])
        #I set a variable to skip the messages outside the loop
        lock_stdout.acquire()
        logger.warning(multiprocessing.current_process().name + ' (worker) Queue empty: exiting')
        lock_stdout.release()
        local_logger.warning(multiprocessing.current_process().name + ' Queue empty: exiting')
    else:
        #I tell the manager that I'm dying because I reached the maximum amount of group to process
        q_life.put(['MAX LIFE REACHED'])
        lock_stdout.acquire()
        logger.warning(multiprocessing.current_process().name + ' (worker) Maximum amount of groups of bibcodes reached: exiting')
        lock_stdout.release()
        local_logger.warning(multiprocessing.current_process().name + ' Maximum amount of groups of bibcodes reached: exiting')
    return


def done_extraction_process(q_done, num_active_workers, lock_stdout, q_life, extraction_directory):
    """Worker that takes care of the groups of bibcodes processed and writes the bibcodes to the related file
        NOTE: this can be also the process that submiths the upload processes to invenio
    """
    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (done bibcodes worker) Process started')
    lock_stdout.release()
    #I create a local logger
    fh = logging.FileHandler(os.path.join(pipeline_settings.BASE_OUTPUT_PATH, extraction_directory, pipeline_settings.BASE_LOGGING_PATH, multiprocessing.current_process().name+'_done_bibcodes.log'))
    fmt = logging.Formatter(pipeline_settings.LOGGING_FORMAT)
    fh.setFormatter(fmt)
    local_logger = logging.getLogger(pipeline_settings.LOGGING_DONE_BIBS_NAME)
    local_logger.addHandler(fh)
    local_logger.setLevel(logger.level)
    local_logger.propagate = False
    #I print the same message for the local logger
    local_logger.warning(multiprocessing.current_process().name + ' Process started')
    
    while(True):
        group_done = q_done.get()

        #first of all I check if the group I'm getting is a message from a process that finished
        if group_done[0] == 'WORKER DONE':
            num_active_workers = num_active_workers - 1
            #if there are no active worker any more, I'm done with processing output
            if num_active_workers == 0:
                break
        else:
            #otherwise I process the output:
            # I puth the bibcodes in the file of the done bibcodes
            if len(group_done[1]) > 0:
                w2f = write_files.WriteFile(extraction_directory, local_logger)
                w2f.write_done_bibcodes_to_file(group_done[1])

                lock_stdout.acquire()
                local_logger.warning(multiprocessing.current_process().name + (' wrote done bibcodes for group %s' % group_done[0]))
                lock_stdout.release()


    #I tell the manager that I'm done and I'm exiting
    q_life.put(['DONEBIBS DONE'])

    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (done bibcodes worker) job finished: exiting')
    lock_stdout.release()
    local_logger.warning(multiprocessing.current_process().name + ' job finished: exiting')
    return


def problematic_extraction_process(q_probl, num_active_workers, lock_stdout, q_life, extraction_directory):
    """Worker that takes care of the bibcodes that couldn't be extracted and writes them to the related file"""
    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (probl. bibcodes worker) Process started')
    lock_stdout.release()
    #I create a local logger
    fh = logging.FileHandler(os.path.join(pipeline_settings.BASE_OUTPUT_PATH, extraction_directory, pipeline_settings.BASE_LOGGING_PATH, multiprocessing.current_process().name+'_probl_bibcodes.log'))
    fmt = logging.Formatter(pipeline_settings.LOGGING_FORMAT)
    fh.setFormatter(fmt)
    local_logger = logging.getLogger(pipeline_settings.LOGGING_PROBL_BIBS_NAME)
    local_logger.addHandler(fh)
    local_logger.setLevel(logger.level)
    local_logger.propagate = False
    #I print the same message for the local logger
    local_logger.warning(multiprocessing.current_process().name + ' Process started')
    
    while(True):
        group_probl = q_probl.get()

        #first of all I check if the group I'm getting is a message from a process that finished
        if group_probl[0] == 'WORKER DONE':
            num_active_workers = num_active_workers - 1
            #if there are no active worker any more, I'm done with processing output
            if num_active_workers == 0:
                break
        else:
            #otherwise I process the output:
            # I puth the bibcodes in the file of the problematic bibcodes
            if len(group_probl[1]) > 0:
                w2f = write_files.WriteFile(extraction_directory, local_logger)
                w2f.write_problem_bibcodes_to_file(group_probl[1])

                local_logger.warning(multiprocessing.current_process().name + (' wrote problematic bibcodes for group %s' % group_probl[0]))

    #I tell the manager that I'm done and I'm exiting
    q_life.put(['PROBLEMBIBS DONE'])

    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (problematic bibcodes worker) job finished: exiting')
    lock_stdout.release()
    local_logger.warning(multiprocessing.current_process().name + ' job finished: exiting')
    return

def upload_process(q_uplfile, lock_stdout, lock_donefiles, q_life, extraction_directory, extraction_name):
    """Worker that uploads the data in invenio"""
    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (upload worker) Process started')
    lock_stdout.release()
    
    #I create a local logger
    fh = logging.FileHandler(os.path.join(pipeline_settings.BASE_OUTPUT_PATH, extraction_directory, pipeline_settings.BASE_LOGGING_PATH, multiprocessing.current_process().name+'_uploader_bibcodes.log'))
    fmt = logging.Formatter(pipeline_settings.LOGGING_FORMAT)
    fh.setFormatter(fmt)
    local_logger = logging.getLogger(pipeline_settings.LOGGING_UPLOAD_NAME)
    local_logger.addHandler(fh)
    local_logger.setLevel(logger.level)
    local_logger.propagate = False
    #I print the same message for the local logger
    local_logger.warning(multiprocessing.current_process().name + ' Process started')
    
    while(True):
        file_to_upload = q_uplfile.get()
        if len(file_to_upload) == 2:
            local_logger.info('Processing group "%s" with file "%s"' % (file_to_upload[0], file_to_upload[1]))
        #first of all I check if the group I'm getting is a message from the manager saying that the workers are done
        if file_to_upload[0] == 'WORKERS DONE':
            local_logger.info('No more workers active: stopping to upload...')
            break
        else:
            #otherwise I have to upload the file
            filepath = file_to_upload[1]
            file_obj = open(filepath, 'rb')
            # I load the object in the file
            local_logger.warning('Upload of the group "%s" started' % file_to_upload[0])
            merged_records = pickle.load(file_obj)
            file_obj.close()
            #finally I upload
            bibupload_merger(merged_records, local_logger, 'replace_or_insert')
            #I log that I uploaded the file
            lock_donefiles.acquire()
            bibrec_file_obj = open(os.path.join(settings.BASE_OUTPUT_PATH, extraction_directory,settings.LIST_BIBREC_UPLOADED), 'a')
            bibrec_file_obj.write(filepath + '\n')
            bibrec_file_obj.close()
            lock_donefiles.release()
            local_logger.warning('Upload of the group "%s" ended' % file_to_upload[0])
            
    #I tell the manager that I'm done and I'm exiting
    q_life.put(['UPLOAD DONE'])

    lock_stdout.acquire()
    logger.warning(multiprocessing.current_process().name + ' (upload worker) job finished: exiting')
    lock_stdout.release()
    local_logger.warning(multiprocessing.current_process().name + ' job finished: exiting')
    return



