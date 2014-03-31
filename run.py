import os, sys
import pymongo
from settings import (CLASSIC_BIBCODES, ARXIV2PUB, MONGO, LOGGER)

import time
from lib import xmltodict
from lib import utils

try:
  import argparse
except ImportError: #argparse not in python2.6, careful!
  from lib import argparse


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--update',
    nargs='*',
    default=CLASSIC_BIBCODES.keys(),
    dest='updateTargets',
    help='Which datasources should be updated'
    )

  args = parser.parse_args()
  LOGGER.debug('Recieved args (%s)' % (args))

  for target in args.updateTargets:
    targetRecords = []
    LOGGER.info('Working on bibcodes in %s' % target)
    
    s = time.time() #Let's eventually use statsd for these timers :)
    with open(CLASSIC_BIBCODES[target]) as fp:
      #Harder to perform set operations on dicts
      #records = [dict(zip(['bibcode','timestamp'],r.strip().split())) for r in fp.readlines() if r and not r.startswith('#')]
      records = [tuple(r.strip().split()) for r in fp.readlines() if r and not r.startswith('#')]
    LOGGER.debug('[%s] Read took %0.1fs' % (target,(time.time()-s)))

    s = time.time()
    targetBibcodes = utils.findChangedRecords(records)
    LOGGER.debug('[%s] Generating list of records to update took %0.1fs' % (target,(time.time()-s)))
    LOGGER.info('[%s] Found %s records to be updated' % (target,len(targetBibcodes)))

    #Eventually could send this list out on the queues as to be non-blocking
    #For now, just work on it here and measure performance
    s = time.time()
    utils.updateRecords(targetBibcodes)
    LOGGER.debug('[%s] Updating %s records took %0.1fs' % (target,len(targetBibcodes),(time.time()-s)))



if __name__ == '__main__':
  try:
    LOGGER.debug('--Start--')
    main()
    LOGGER.debug('--End--')
  except SystemExit:
    pass #this exception is raised by argparse if -h or wrong args given; we will ignore.
  except:
    LOGGER.exception('Traceback:')
    raise