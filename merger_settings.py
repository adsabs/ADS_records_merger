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
@author: Giovanni Di Milia and Benoit Thiell
File containing all the settings for the merger: priority lists and other
'''

import time

VERBOSE = True

#########################
#SUBFIELDS DEFINITION

#subfield containing the origin
ORIGIN_SUBFIELD = '8'
#subfield containing the Author normalized name
AUTHOR_NORM_NAME_SUBFIELD = 'b'
#subfields for keywords
KEYWORD_STRING_SUBFIELD = 'a'
KEYWORD_ORIGIN_SUBFIELD = '9'
#subfields for references
REFERENCE_RESOLVED_KEY = 'i'
REFERENCE_STRING = 'b'
#subfields for creation and modification date
CREATION_DATE_SUBFIELD = 'x'
MODIFICATION_DATE_SUBFIELD = 'c'
#subfield for system number 
SYSTEM_NUMBER_SUBFIELD = 'a'
#subfield for publication date 
PUBL_DATE_SUBFIELD = 'c'
PUBL_DATE_TYPE_SUBFIELD = 't'
PUBL_DATE_TYPE_VAL_SUBFIELD = ('date-published', 'date-preprint', 'date-reprint', 'date-erratum', 'date-thesis', 'date-submitted', 'date-accepted')

#########################

#mapping between the marc field and the name of the field
MARC_TO_FIELD = {
     '024': 'doi',
     '035': 'identifiers',
     '041': 'language code',
     '100': 'first author',
     '242': 'title translation',
     '245': 'original title',
     '260': 'publication date',
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

#mapping between the field and the marc field
FIELD_TO_MARC = dict([v,k] for k,v in MARC_TO_FIELD.items())

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
    'creation and modification date': 'merging_rules.take_all',
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
    'publication date': 'merging_rules.pub_date_merger', 
    'references': 'merging_rules.references_merger',
    'system number': 'merging_rules.priority_based_merger',
    'theses': 'merging_rules.take_all',
    'timestamp': 'merging_rules.priority_based_merger',
    'title translation': 'merging_rules.title_merger',
}

#checks and specific errors that should be applied during a merging
#any function points to a list of subfield where it should be applied
#if this list is empty then the function should be applied on the entire field 
#that can mean "any subfield" or the fields as a whole 
MERGING_RULES_CHECKS_ERRORS = {
    'original title': {
        'warnings': {
            'merging_checks.check_string_with_unicode_not_selected' : ['a'],
            'merging_checks.check_longer_string_not_selected': ['a'],
            'merging_checks.check_uppercase_string_selected': ['a'],
            #'merging_checks.no_field_chosen_with_available_fields': ['a'], #this check seems to be useless
        }
    },
    'first author': {
        'warnings': {
            'merging_checks.check_author_from_shorter_list': [],
        },
    },
    'other author': {
        'warnings': {
            'merging_checks.check_author_from_shorter_list': [],
            'merging_checks.check_duplicate_normalized_author_names': [],
        },
    },
    'journal': {
        'warnings': {
            'merging_checks.check_longer_string_not_selected': ['p', 'z'],
        },
    },
    'free keyword': {
        'warnings': {
            'merging_checks.check_different_keywords_for_same_type': [],
        },
    },
    'controlled keywords': {
        'warnings': {
            'merging_checks.check_different_keywords_for_same_type': [],
        },
    },
    'abstract': {
        'warnings': {
            'merging_checks.check_string_with_unicode_not_selected': ['a'],
            'merging_checks.check_longer_string_not_selected': ['a'],
            #'merging_checks.no_field_chosen_with_available_fields': [], #this check seems to be useless
        }
    },
    'publication date': {
        'warnings': {
            'merging_checks.check_pubdate_without_month_selected': ['c'],
            'merging_checks.check_one_date_per_type': [('c','t')], #in this particular case the order of the two subfields is really important
        }               
    }
}

#list of merging function to apply to the entire record
GLOBAL_MERGING_RULES = [
    'global_merging_rules.merge_creation_modification_dates'
]
#list of merging checks to apply to the entire record
GLOBAL_MERGING_CHECKS = {
    'warnings': [                    
        'global_merging_checks.check_pub_year_consistency'
    ]
}


#If there is a specific priority list per one field its name should be specified here (see example)
#if not specified the standard one will be applied
FIELDS_PRIORITY_LIST = {
    'references': 'references_priority_list',
    #'doi': 'doi_priority_list',
}

#name of the default_priority_list
DEFAULT_PRIORITY_LIST = 'standard_priority_list'

#priority lists
__PRIORITIES = {
    10: ['ADS METADATA',],
    1.0: ['ISI'],
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
        'SerAJ', 'T+F', 'TERRAPUB', 'UCP', 'UMI', 'USCI', 'USNO',
        'VATICAN', 'VERSITA', 'WGN', 'WILEY', 'WSPC', 'XMM', 'XTE',],
    0.45: ['ARI', 'ARIBIB', 'ARXIV', 'JSTOR',],
    0.4: ['CARL', 'CFA', 'HOLLIS', 'LIBRARY', 'POS', 'PRINCETON', 'SIMBAD',
        'STSCI', 'UTAL',],
    0.375: ['STI', 'WEB',],
    0.35: ['AP', 'CROSSREF', 'GCPD', 'GONG', 'KNUDSEN', 'METBASE',],
    0.3: ['OCR',],
    0.25: ['NED',],
}

__PRIORITIES_REFERENCES = {
    10:  ['AUTHOR',],
    9.5: ['ISI',],
    9.1: ['SPRINGER',],
    9:   ['A&A', 'A&AS', 'A&G', 'AAO', 'AAS', 'AASP', 'AAVSO', 'ACA',
        'ACASN', 'ACHA', 'ACTA', 'ADASS', 'ADIL', 'ADS', 'AFRSK', 'AG',
        'AGDP', 'AGU', 'AIP', 'AJ', 'ALMA', 'AMS', 'AN', 'ANRFM', 'ANRMS',
        'APJ', 'APS', 'ARA&A', 'ARAA', 'ARAC', 'AREPS', 'ARNPS', 'ASBIO',
        'ASD', 'ASL', 'ASP', 'ASPC', 'ASTL', 'ASTRON', 'ATEL', 'ATSIR',
        'BAAA', 'BAAS', 'BALTA', 'BASBR', 'BASI', 'BAVSR', 'BEO',
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
        'SPIE', 'SPIKA', 'SPITZER', 'SPRN', 'STARD', 'STECF',
        'STSCI', 'SerAJ', 'T+F', 'TERRAPUB', 'UCP', 'UMI', 'USCI', 'USNO',
        'VATICAN', 'VERSITA', 'WGN', 'WILEY', 'WSPC', 'XMM', 'XTE'
        'ARI', 'ARIBIB', 'JSTOR', 'CARL', 'CFA', 'HOLLIS', 'LIBRARY', 
        'POS', 'PRINCETON', 'SIMBAD','UTAL', 'STI', 'WEB',
        'AP', 'GCPD', 'GONG', 'KNUDSEN', 'METBASE', 'NED',],
    8.9: ['PUBLISHER'],
    8.5: ['OCR', 'ADS METADATA'],
    8:   ['CROSSREF',],
    5:   ['ARXIV',],
}

PRIORITIES = {
    'standard_priority_list': dict((source, score)
        for score, sources in __PRIORITIES.items()
        for source in sources),
    'references_priority_list': dict((source, score)
        for score, sources in __PRIORITIES_REFERENCES.items()
        for source in sources),
}

#list of origins for which we have to apply the take_all
#for all the others will be applied the priority_merging
#the two groups will be merged with a take all
REFERENCES_MERGING_TAKE_ALL_ORIGINS = ['ISI', 'AUTHOR', 'CROSSREF']


def msg(message, verbose=VERBOSE):
    """
    Prints a debug message.
    """
    if verbose:
        print time.strftime("%Y-%m-%d %H:%M:%S"), '---', message


def manage_check_error(msg_str, type_check):
    """function that prints a warning or 
    raises an exception according to the type of check"""
    
    from merger_errors import GenericError
    
    if type_check == 'warnings':
        msg('          CHECK WARNING: %s' % msg_str , True)
    elif type_check == 'errors':
        raise GenericError(msg_str)
    else:
        raise GenericError('Type of check "%s" cannot be handled by the "manage_check_error" function.')
    return None