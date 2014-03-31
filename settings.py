import os
import sys

import logging
from logging.handlers import RotatingFileHandler

PROJECT_HOME = os.path.abspath(os.path.dirname(__file__))
LOGFILE = os.path.join(PROJECT_HOME,'logs','merger.log')
LOG_LEVEL = logging.DEBUG
#LOG_LEVEL = logging.INFO

CLASSIC_BIBCODES = {
  'AST': '/proj/ads/abstracts/ast/load/current/index.status',
  'PHY': '/proj/ads/abstracts/phy/load/current/index.status',
  'GEN': '/proj/ads/abstracts/gen/load/current/index.status',
  'PRE': '/proj/ads/abstracts/pre/load/current/index.status'
}

ARXIV2PUB = '/proj/ads/abstracts/config/links/preprint/arxiv2pub.list'

MONGO = {
  'HOST': os.environ.get('MONGO_HOST','localhost'),
  'PORT': os.environ.get('MONGO_PORT',27017),
  'DATABASE': os.environ.get('MONGO_DATABSE','invenio'),
  'USER': None,    #May be set to None
  'PASSWD': None,  #May be set to None
  'COLLECTION': 'marc',

}
auth = ''
if MONGO['USER'] and MONGO['PASSWD']:
  auth =  '%s@' % (':'.join([MONGO['USER'],MONGO['PASSWD']]))
MONGO['MONGO_URI'] = 'mongodb://%s%s:%s' % (auth,MONGO['HOST'],MONGO['PORT'])

FIELDS = [
  'isbn',
  'issn',
  'doi',
  'identifiers',
  'language code',
  'first author',
  'conference_metadata',
  'title translation',
  'original title',
  'publication date',
  'number of pages',
  'comment',
  'theses',
  'abstract',
  'copyright',
  'associate papers',
  'arxiv tags',
  'free keyword',
  'facility telescope instrument',
  'objects',
  'controlled keywords',
  'other author',
  'collaboration',
  'journal',
  'other journal',
  'link',
  'origin',
  'creation and modification date',
  'system number',
  'collection',
  'timestamp',
  'references',
]

MERGING_RULES = {
  'abstract': 'merging_rules.abstract_merger',
  'arxiv tags': 'merging_rules.priority_based_merger',
  'associate papers': 'merging_rules.priority_based_merger',
  'collaboration': 'merging_rules.priority_based_merger',
  'collection': 'merging_rules.priority_based_merger',
  'comment': 'merging_rules.take_all',
  'conference_metadata': 'merging_rules.priority_based_merger',
  'controlled keywords': 'merging_rules.take_all',
  'copyright': 'merging_rules.priority_based_merger',
  'creation and modification date': 'merging_rules.take_all',
  'doi': 'merging_rules.priority_based_merger',
  'facility telescope instrument': 'merging_rules.take_all',
  'first author': 'merging_rules.author_merger',
  'free keyword': 'merging_rules.take_all',
  'identifiers': 'merging_rules.take_all',
  'isbn' : 'merging_rules.take_all',
  'issn' : 'merging_rules.take_all',
  'journal': 'merging_rules.priority_based_merger',
  'language code': 'merging_rules.priority_based_merger',
  'link': 'merging_rules.priority_based_merger',
  'number of pages': 'merging_rules.priority_based_merger',
  'objects' : 'merging_rules.take_all',
  'origin' : 'merging_rules.priority_based_merger',
  'original title': 'merging_rules.title_merger',
  'other author': 'merging_rules.author_merger',
  'other journal': 'merging_rules.take_all',
  'publication date': 'merging_rules.pub_date_merger',
  'references': 'merging_rules.references_merger',
  'system number': 'merging_rules.priority_based_merger',
  'theses': 'merging_rules.take_all',
  'timestamp': 'merging_rules.priority_based_merger',
  'title translation': 'merging_rules.title_merger',
}



logfmt = '%(levelname)s [%(asctime)s]:\t %(message)s'
datefmt= '%m/%d/%Y %I:%M:%S %p'
formatter = logging.Formatter(fmt=logfmt,datefmt=datefmt)
LOGGER = logging.getLogger('ADS_records_merger')
logging.root.setLevel(LOG_LEVEL)
rfh = RotatingFileHandler(filename=LOGFILE,maxBytes=2097152,backupCount=3,mode='a') #2MB file
rfh.setFormatter(formatter)
ch = logging.StreamHandler() #console handler
ch.setFormatter(formatter)
LOGGER.handlers = []
LOGGER.addHandler(ch)
LOGGER.addHandler(rfh)