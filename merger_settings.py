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
@author: Giovanni Di Milia,
File containing all the settings for the merger: priority lists and other
'''

import time

#subfield containing the origin
ORIGIN_SUBFIELD = '8'

#mapping between the marc field and the name of the field
MARC_TO_FIELD = {
     '024': 'doi',
     '035': 'identifiers',
     '041': 'language code',
     '100': 'first author',
     '242': 'title translation',
     '245': 'original title',
     '260': 'publication date',
     '269': 'preprint date',
     '300': 'number of pages',
     '500': 'comment',
     '502': 'theses',
     '520': 'abstract',
     '540': 'copyright',
     '591': 'associate papers',
     '650': 'arxiv tags',
     '653': 'free keyword',
     '693': 'facility telescope',
     '695': 'controlled keywords',
     '700': 'other author',
     '710': 'collaboration',
     '773': 'journal',
     '856': 'link',
     '961': 'creation and modification date',
     '970': 'system number',
     '980': 'collection',
     '995': 'timestamp',
     '999': 'references',
}

#merging rule function associated with the single fields
MERGING_RULES = {
    'abstract': 'merging_rules.abstract_merger',
    'arxiv tags': 'merging_rules.priority_based_merger',
    'associate papers': 'merging_rules.priority_based_merger',
    'collaboration': 'merging_rules.priority_based_merger',
    'collection': 'merging_rules.priority_based_merger',
    'comment': 'merging_rules.take_all',
    'controlled keywords': 'merging_rules.take_all',
    'copyright': 'merging_rules.priority_based_merger',
    'creation and modification date': 'merging_rules.priority_based_merger',
    'doi': 'merging_rules.priority_based_merger',
    'facility telescope': 'merging_rules.priority_based_merger',
    'first author': 'merging_rules.author_merger',
    'free keyword': 'merging_rules.take_all',
    'identifiers': 'merging_rules.take_all',
    'journal': 'merging_rules.priority_based_merger',
    'language code': 'merging_rules.priority_based_merger',
    'link': 'merging_rules.priority_based_merger',
    'number of pages': 'merging_rules.priority_based_merger',
    'original title': 'merging_rules.title_merger',
    'other author': 'merging_rules.author_merger',
    'preprint date': 'merging_rules.priority_based_merger',
    'publication date': 'merging_rules.priority_based_merger',
    'references': 'merging_rules.priority_based_merger',
    'system number': 'merging_rules.priority_based_merger',
    'theses': 'merging_rules.take_all',
    'timestamp': 'merging_rules.priority_based_merger',
    'title translation': 'merging_rules.title_merger',
}

#checks and specific errors that should be applied during a merging
MERGING_RULES_CHECKS_ERRORS = {
        'original title': {
            'warnings': ['merging_checks.string_with_unicode_not_selected',
                'merging_checks.longer_string_not_selected',
                'merging_checks.uppercase_string_selected',
                'merging_checks.no_field_chosen_with_available_fields']
            },
        'first author': {
            'warnings': ['merging_checks.author_from_shorter_list'],
            },
        'other author': {
            'warnings': ['merging_checks.author_from_shorter_list'],
            },
        'journal': {
            'warnings': ['merging_checks.pubdate_without_month_selected',
                'merging_checks.pubdate_no_match_year_bibcode',
                'merging_checks.different_pubdates'],
            },
        'free keyword': {
            'warnings': ['merging_checks.different_keywords_for_same_type']
            },
        'controlled keywords': {
            'warnings': ['merging_checks.different_keywords_for_same_type']
            },
        'abstract': {
            'warnings': ['merging_checks.string_with_unicode_not_selected',
                'merging_checks.longer_string_not_selected',
                'merging_checks.no_field_chosen_with_available_fields']
            },
        }

#If there is a specific priority list per one field its name should be specified here (see example)
#if not specified the standard one will be applied
FIELDS_PRIORITY_LIST = {
    #'doi': 'doi_priority_list',
}

#name of the default_priority_list
DEFAULT_PRIORITY_LIST = 'standard_priority_list'

#priority lists
__PRIORITIES = {
        10: ['ADS metadata',],
        0.5: ['A&A', 'A&AS', 'A&G', 'AAO', 'AAS', 'AASP', 'AAVSO', 'ACA',
            'ACASN', 'ACHA', 'ACTA', 'ADASS', 'ADIL', 'ADS', 'AFRSK', 'AG',
            'AGDP', 'AGU', 'AIP', 'AJ', 'ALMA', 'AMS', 'AN', 'ANRFM', 'ANRMS',
            'APJ', 'APS', 'ARA&A', 'ARAA', 'ARAC', 'AREPS', 'ARNPS', 'ASBIO',
            'ASD', 'ASL', 'ASP', 'ASPC', 'ASTL', 'ASTRON', 'ATEL', 'ATSIR',
            'AUTHOR', 'BAAA', 'BAAS', 'BALTA', 'BASBR', 'BASI', 'BAVSR', 'BEO',
            'BESN', 'BLAZ', 'BLGAJ', 'BOTT', 'BSSAS', 'CAPJ', 'CBAT', 'CDC',
            'CEAB', 'CFHT', 'CHAA', 'CHANDRA', 'CHJAA', 'CIEL', 'COAST',
            'COPERNICUS', 'COSKA', 'CSCI', 'CUP', 'CXC', 'CXO', 'DSSN',
            'E&PSL', 'EDP', 'EJTP', 'ELSEVIER', 'ESA', 'ESO', 'ESP', 'EUVE',
            'FCPH', 'FUSE', 'GCN', 'GJI', 'GRG', 'HISSC', 'HST', 'HVAR', 'IAJ',
            'IAU', 'IAUC', 'IAUDS', 'IBVS', 'ICAR', 'ICQ', 'IMO', 'INGTN',
            'IOP', 'ISAS', 'ISSI', 'IUE', 'JAA', 'JAD', 'JAHH', 'JAPA', 'JASS',
            'JAVSO', 'JBAA', 'JENAM', 'JHA', 'JIMO', 'JKAS', 'JPSJ', 'JRASC',
            'JSARA', 'JST', 'KFNT', 'KITP', 'KLUWER', 'KOBV', 'KON', 'LNP',
            'LOC', 'LPI', 'LRR', 'LRSP', 'M&PS', 'M+PS', 'METIC', 'MIT',
            'MNRAS', 'MNSSA', 'MOLDAVIA', 'MPBU', 'MPC', 'MPE', 'MPSA',
            'MmSAI', 'NAS', 'NATURE', 'NCSA', 'NEWA', 'NOAO', 'NRAO', 'NSTED',
            'O+T', 'OAP', 'OBS', 'OEJV', 'OSA', 'PABEI', 'PADEU', 'PAICU',
            'PAICz', 'PAOB', 'PASA', 'PASJ', 'PASP', 'PDS', 'PHIJA', 'PHYS',
            'PJAB', 'PKAS', 'PLR', 'PNAS', 'POBEO', 'PSRD', 'PTP', 'PZP',
            'QJRAS', 'RMXAA', 'RMXAC', 'ROAJ', 'RVMA', 'S&T', 'SABER', 'SAI',
            'SAJ', 'SAO', 'SAS', 'SCI', 'SCIENCE', 'SERB', 'SF2A', 'SLO',
            'SPIE', 'SPIKA', 'SPITZER', 'SPRINGER', 'SPRN', 'STARD', 'STECF',
            'STSCI', 'SerAJ', 'T+F', 'TERRAPUB', 'UCP', 'UMI', 'USCI', 'USNO',
            'VATICAN', 'VERSITA', 'WGN', 'WILEY', 'WSPC', 'XMM', 'XTE',],
        0.45: ['ARI', 'ARIBIB', 'ARXIV', 'JSTOR',],
        0.4: ['CARL', 'CFA', 'HOLLIS', 'LIBRARY', 'POS', 'PRINCETON', 'SIMBAD',
            'STSci', 'UTAL',],
        0.375: ['STI', 'WEB',],
        0.35: ['AP', 'CROSSREF', 'GCPD', 'GONG', 'KNUDSEN', 'METBASE',],
        0.3: ['OCR',],
        0.25: ['NED',],
        }

PRIORITIES = {
        'standard_priority_list': dict((source, score)
            for score, sources in __PRIORITIES.items()
            for source in sources)
}

VERBOSE = True

def msg(message, verbose=VERBOSE):
    """
    Prints a debug message.
    """
    if verbose:
        print time.strftime("%Y-%m-%d %H:%M:%S"), '---', message
