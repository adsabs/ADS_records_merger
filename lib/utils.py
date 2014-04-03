import os,sys
import pymongo
import time
import itertools
import json
import copy

from settings import (MONGO,LOGGER)
from rules import merger
from lib import xmltodict
from lib import collections

try:
  from ads.ADSExports import ADSRecords
except ImportError:
  sys.path.append('/proj/ads/soft/python/lib/site-packages')
  from ads.ADSExports import ADSRecords

def init_db(db):
  db[MONGO['COLLECTION']].ensure_index('bibcode',unique=True)

def mongoCommit(records):
  if not records:
    return False
  conn = pymongo.MongoClient(host=MONGO['MONGO_URI'])
  db = conn[MONGO['DATABASE']]
  if MONGO['COLLECTION'] not in db.collection_names():
    init_db(db)
  collection = db[MONGO['COLLECTION']]
  for r in records:
    assert(r['bibcode'])
    assert(r['JSON_fingerprint'])
    #query = {"bibcode": {"$in": [r['bibcode'] for r in records]}}
    query = {"bibcode": r['bibcode']}
    collection.update(query,r,upsert=True,w=1,multi=False) #w=1 means block all write requests until it has written to the primary
  conn.close()

def findChangedRecords(records):
  if not records:
    LOGGER.debug("No records given")
    return []

  conn = pymongo.MongoClient(host=MONGO['MONGO_URI'])
  db = conn[MONGO['DATABASE']]

  if MONGO['COLLECTION'] not in db.collection_names():
    init_db(db)
  collection = db[MONGO['COLLECTION']]
  res = list(collection.find({"bibcode": {"$in": [rec[0] for rec in records]}}))
  currentRecords = [(r['bibcode'],r['JSON_fingerprint']) for r in collection.find({"bibcode": {"$in": [rec[0] for rec in records]}})]
  conn.close()
  return list(set(records).difference(currentRecords))

def updateRecords(records):
  if not records:
    LOGGER.debug("No records given")
    return []

  targets = dict(records)


  s = time.time()
  records = ADSRecords('full','XML')
  failures = []
  for bibcode in targets.keys():
    try:
      records.addCompleteRecord(bibcode)
    except:
      failures.append(bibcode)
      LOGGER.debug("[%s] ADSRecords failed" % bibcode)
  records = records.export()
  if not records.content:
    return []
  ttc = time.time()-s
  rate = len(targets)/ttc
  LOGGER.warning('ADSRecords failed to retrieve %s records' % len(failures))
  LOGGER.info('ADSRecords took %0.1fs to query %s records (%0.1f rec/s)' % (ttc,len(targets),rate))

  records = xmltodict.parse(records.__str__())['records']['record']
  assert(len(records)==len(targets)-len(failures))

  #Could send these tasks out on a queue
  completeRecords = []
  for r in records:
    #Define top-level schema
    cr = {
      'bibcode': r['@bibcode'],
      'JSON_fingerprint': targets[r['@bibcode']],
      'metadata' : {},
    }

    #Find metadata blocks that need merging
    metadataCounter = collections.Counter([entry['@type'] for entry in r['metadata']])
    needsMerging = dict([(k,[]) for k,v in metadataCounter.iteritems() if v>1])

    #Iterate over metadata blocks; directly input single defined blocks
    #and build a 'needsMerging' list to merge in the next step
    for entry in r['metadata']: 
      if metadataCounter[entry['@type']] not in needsMerging:
        cr['metadata'].update({entry['@type']:entry})
      else: #If it shows up more than once, it needs merging.
        needsMerging[entry['@type']].append(entry)

    for entryType,data in needsMerging.iteritems():
      cr['metadata'].update({entryType:merge(data)})

    completeRecords.append(cr)

  LOGGER.debug('Added %s complete records' % len(completeRecords))
  return completeRecords

def enforceSchema(records):
  '''
  translates schema from ADSRecords to alternative schema
  '''

  return records

def merge(metadataBlocks):
  '''
  Merges multiply defined fields within a list of <metadata> blocks
  Returns a single (merged) <metadata> block
  '''

  fieldsHist = collections.Counter([i for i in list(itertools.chain(*metadataBlocks)) if not i.startswith('@')])
  singleDefinedFields = [k for k,v in fieldsHist.iteritems() if v==1]
  multipleDefinedFields = [k for k,v in fieldsHist.iteritems() if v>1]

  #Create intermediate data structure that lets us easily iterate over those fields that merging
  fields = {}
  for block in metadataBlocks:
    for fieldName,content in block:
      if fieldName not in multipleDefinedFields:
        continue
      if fieldName not in fields:
        fields[fieldName] = []
      fields[fieldName].append({
        '@origin':block['@origin'],
        'content':data
      })

  #Merge those fields that are multiply defined      
  mergedResults = {}
  for fieldName,data in fields:
    results = None
    while len(data) > 1:
      f1 = data.pop()
      f2 = result if result else data.pop()
      results = merger.dispatcher(f1,f2,fieldName)
    mergedResults[fieldName] = result

  #Combine all the pieces into the complete <metadata> block
  completeBlock = {}
  singleDefined = dict([(k,v) for block in metadataBlocks for k,v in block.iteritems() if k in singleDefinedFields])
  completeBlock.update(singleDefined)
  completeBlock.update(mergedResults)

  return completeBlock
