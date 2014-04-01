import os,sys
import pymongo
import time
import collections
import json

from ..settings import (MONGO,LOGGER)
from ..rules import merger_rules
from ..lib import xmltodict

try:
  from ads.ADSExports import ADSRecords
except ImportError:
  sys.path.append('/proj/ads/soft/python/lib/site-packages')
  from ads.ADSExports import ADSRecords

def init_db(db):
  db[MONGO['COLLECTION']].ensure_index('bibcode',unique=True)

def mongoCommit(records):

  conn = pymongo.MongoClient(host=MONGO['MONGO_URI'])
  db = conn[MONGO['DATABASE']]

  if MONGO['COLLECTION'] not in db.collection_names():
    init_db(db)
  collection = db[MONGO['COLLECTION']] 
  #db.update(query,json.dumps(records),upsert=True)


def findChangedRecords(records):
  if not records:
    LOGGER.debug("No records given")
    return

  conn = pymongo.MongoClient(host=MONGO['MONGO_URI'])
  db = conn[MONGO['DATABASE']]

  if MONGO['COLLECTION'] not in db.collection_names():
    init_db(db)
  collection = db[MONGO['COLLECTION']]

  currentRecords = [(r['bibcode'],r['JSON_fingerprint']) for r in collection.find({"bibcode": {"$in": [rec[0] for rec in records]}})]

  db.close()
  return [i[0] for i in set(records).difference(currentRecords)]

def updateRecords(records):
  if not records:
    LOGGER.debug("No records given")
    return

  targets = dict(records)

  s = time.time()
  records = ADSRecords('full','XML')
  [records.addCompleteRecord(bibcode) for bibcode,JSON_fingerprint in targets.iteritems()]
  records = records.export()
  ttc = time.time()-s
  rate = ttc/len(bibcodes)
  LOGGER.info('ADSRecords took %0.1fs to gather %s records (%0.1f rec/s)' % (ttc,len(bibcodes),rate))

  records = xmltodict.parse(records.__str__())['records']['record']

  #Reformat output to be in {'<bibcode>':[{'author':...}.],} format
  formattedRecords = {}
  for r in records:
    bibcode = r['@bibcode']
    if bibcode not in formattedRecords:
      formattedRecords[bibcode] = []
    formattedRecords[bibcode].append(r['metadata'])
  assert(len(formattedRecords)==len(bibcodes))

  #Could send these tasks out on a queue
  completeRecords = []
  for bibcode,records in formattedRecords.iteritems():
    cr = {'bibcode':bibcode,
          'JSON_fingerprint': targets[bibcode]}

    #Add fields that only show up once
    fieldsHist = collections.Counter(records).items()
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
    mergedRecords.append(cr)

  LOGGER.debug('Added %s complete records' % len(completeRecords))
  return mergedRecords

def merge(fieldsDict):
  tag,fields = fieldsDict.items()
  result = None
  while len(fields) > 1:
    f1 = fields.pop()
    f2 = result if result else fields.pop()
    result = rules.dispatcher(f1,f2,tag)