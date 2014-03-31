import os,sys
import pymongo
import time

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../'))
from settings import (MONGO,LOGGER)
from rules import merger_rules
from lib import xmltodict

try:
  from ads.ADSExports import ADSRecords
except ImportError:
  sys.path.append('/proj/ads/soft/python/lib/site-packages')
  from ads.ADSExports import ADSRecords

def init_db(db):
  db[MONGO['COLLECTION']].ensure_index('bibcode',unique=True)

def findChangedRecords(records):
  conn = pymongo.MongoClient(host=MONGO['MONGO_URI'])
  db = conn[MONGO['DATABASE']]

  if MONGO['COLLECTION'] not in db.collection_names():
    init_db(db)
  collection = db[MONGO['COLLECTION']]

  currentRecords = [(r['bibcode'],r['JSON_fingerprint']) for r in collection.find({"bibcode": {"$in": [rec[0] for rec in records]}})]

  db.close()
  return [i[0] for i in set(records).difference(currentRecords)]

def updateRecords(bibcodes):
  s = time.time()
  records = ADSRecords('full','XML')
  [records.addCompleteRecord(b) for b in bibcodes]
  records = records.export()
  ttc = time.time()-s
  rate = ttc/len(bibcodes)
  LOGGER.info('ADSRecords took %0.1fs to gather %s records (%0.1f rec/s)' % (ttc,len(bibcodes),rate))

  records = xmltodict.parse(records.__str__())['records']['record']
  assert(len(records)>=len(bibcodes)) #Weak assertion











