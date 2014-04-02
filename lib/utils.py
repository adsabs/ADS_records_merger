import os,sys
import pymongo
import time
import itertools
import json

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

  #Reformat output to be in {'<bibcode>':[{'author':...}.],} format
  formattedRecords = {}
  for r in records:
    bibcode = r['@bibcode']
    if bibcode not in formattedRecords:
      formattedRecords[bibcode] = []
    formattedRecords[bibcode].extend(r['metadata'])
  assert(len(formattedRecords)==len(targets)-len(failures))

  #Could send these tasks out on a queue
  completeRecords = []
  for bibcode,records in formattedRecords.iteritems():
    #Add fields that only show up once
    cr = {}
    fieldsHist = collections.Counter(list(itertools.chain(*records))).items()
    singlyDefinedFields = [k for k,v in fieldsHist if v==1 and not k.startswith('@')]
    for record in records:
      for field in singlyDefinedFields:
        if field in record.keys():
          #Could add a translation layer here if we want to re-name the fields in our mongo collection
          cr.update({field:record[field]})

    #Fields with more than one entry need merging.
    multipleDefinedFields = [k for k,v in fieldsHist if v>1 and not k.startswith('@')]
    needsMerging = {}
    for field in multipleDefinedFields:
      needsMerging[field] = []
      for record in records:
        if field in record.keys():
          needsMerging[field].append(record[field])
      cr.update({field:merge(needsMerging)})
    cr.update({'bibcode':bibcode,'JSON_fingerprint': targets[bibcode]})
    completeRecords.append(cr)

  LOGGER.debug('Added %s complete records' % len(completeRecords))
  return completeRecords

def merge(fieldsDict):
  tag,fields = tuple(fieldsDict.items())[0]
  result = None
  while len(fields) > 1:
    f1 = fields.pop()
    f2 = result if result else fields.pop()
    result = merger.dispatcher(f1,f2,tag)
  return result