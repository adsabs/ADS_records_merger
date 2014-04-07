from __future__ import absolute_import
try:
  from proj.celery import app
except:
  pass
import time
import os,sys
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(PROJECT_HOME)
from lib import utils

#@recordMergerPipeline.task
def processRecords(records,LOGGER,MONGO):
  '''
  Task that performs the following tasks:
    . Takes a list of bibcodes from rabbitmq
    . Runs ADSExports to gather data on each bibcodes
    . Checks mongodb for records that need updating
    . Merges any duplicated <metadata> tags
    . Upserts data to mongodb
  '''
  print "Here"
  s = time.time()
  records = utils.findChangedRecords(records,LOGGER,MONGO)
  LOGGER.debug('[%s] Generating list of records to update took %0.1fs' % (target,(time.time()-s)))
  LOGGER.info('[%s] Found %s records to be updated' % (target,len(records)))

  #Eventually could send this list out on the queues as to be non-blocking
  #For now, just work on it here and measure performance
  s = time.time()
  records = utils.updateRecords(records,LOGGER)
  LOGGER.info('[%s] Updating %s records took %0.1fs' % (target,len(records),(time.time()-s)))

  records = utils.enforceSchema(records,LOGGER)

  s = time.time()
  utils.mongoCommit(records,LOGGER,MONGO)
  LOGGER.info('Write %s records to mongo took %0.1fs' % (len(records),(time.time()-s)))