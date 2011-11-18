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

#importing the merging rules
from merging_rules import priority_based_merger, take_all, author_merger,\
    title_merger, abstract_merger
#and the merging checks
from merging_checks import string_with_unicode_not_selected, \
    longer_string_not_selected, uppercase_string_selected, no_field_chosen_with_available_fields,\
    author_from_shorter_list, pubdate_without_month_selected, pubdate_no_match_year_bibcode,\
    different_pubdates, different_keywords_for_same_type

#mapping between the marc field and the name of the field 
MARC_TO_FIELD = {
     '024' : 'doi',
     '035' : 'identifiers',
     '041' : 'language code',
     '100' : 'first author',
     '242' : 'title translation',
     '245' : 'original title',
     '260' : 'publication date',
     '269' : 'preprint date',
     '300' : 'number of pages',
     '500' : 'comment',
     '502' : 'theses',
     '520' : 'abstract',
     '540' : 'copyright',
     '591' : 'associate papers',
     '650' : 'arxiv tags',
     '653' : 'free keyword',
     '693' : 'facility telescope',
     '695' : 'controlled keywords',
     '700' : 'other author',
     '710' : 'collaboration',
     '773' : 'journal',
     '856' : 'link',
     '961' : 'creation and modification date',
     '970' : 'system number',
     '980' : 'collection',
     '995' : 'timestamp',
     '999' : 'references'
}

#merging rule function associated with the single fields
MERGING_RULES = {
    'doi' : priority_based_merger,
    'identifiers': take_all,
    'language code': priority_based_merger,
    'first author' : author_merger,
    'title translation' : title_merger,
    'original title' : title_merger,
    'publication date' : priority_based_merger,
    'preprint date' : priority_based_merger,
    'number of pages' : priority_based_merger,
    'comment' : take_all,
    'theses' : take_all,
    'abstract' : abstract_merger,
    'copyright' : priority_based_merger,
    'associate papers' : priority_based_merger,
    'arxiv tags' : priority_based_merger,
    'free keyword' : take_all,
    'facility telescope' : priority_based_merger,
    'controlled keywords' : take_all,
    'other author' : author_merger,
    'collaboration' : priority_based_merger,
    'journal' : priority_based_merger,
    'link' : priority_based_merger,
    'creation and modification date' : priority_based_merger,
    'system number' : priority_based_merger,
    'collection' : priority_based_merger,
    'timestamp' : priority_based_merger,
    'references' : priority_based_merger
}

#checks and specific errors that should be applied during a merging
MERGING_RULES_CHECKS_ERRORS = {
    'original title' : {
        'warnings' : [string_with_unicode_not_selected, longer_string_not_selected, uppercase_string_selected, no_field_chosen_with_available_fields]
    },
    'first author' : {
        'warnings' : [author_from_shorter_list],
    },
    'other author' : {
        'warnings' : [author_from_shorter_list],
    },
    'journal' : {
        'warnings' : [pubdate_without_month_selected, pubdate_no_match_year_bibcode, different_pubdates], 
    },
    'free keyword' : {
        'warnings' : [different_keywords_for_same_type]
    },
    'controlled keywords' : {
        'warnings' : [different_keywords_for_same_type]
    },
    'abstract' : {
        'warnings' : [string_with_unicode_not_selected, longer_string_not_selected, no_field_chosen_with_available_fields]
    },
}

#If there is a specific priority list per one field its name should be specified here (see example)
#if not specified the standard one will be applied
FIELDS_PRIORITY_LIST = {
    #'doi' : 'doi_priority_list',
}

#priority lists
PRIORITY_LISTS = {
    'standard_priority_list' : {'NOAO': '0.5', 'BLAZ': '0.5', 'BESN': '0.5', 'EJTP': '0.5', 'HVAR': '0.5', 'KITP': '0.5', 'NAS': '0.5', 
                                'ARAA': '0.5', 'VATICAN': '0.5', 'USCI': '0.5', 'ELSEVIER': '0.5', 'AGU': '0.5', 'JAVSO': '0.5', 
                                'MIT': '0.5', 'SAJ': '0.5', 'SAI': '0.5', 'MPBU': '0.5', 'MPSA': '0.5', 'RMXAC': '0.5', 'ADIL': '0.5', 
                                'RMXAA': '0.5', 'PZP': '0.5', 'IOP': '0.5', 'ROAJ': '0.5', 'STSCI': '0.5', 'HST': '0.5', 'SAS': '0.5', 
                                'JBAA': '0.5', 'BASI': '0.5', 'JASS': '0.5', 'IBVS': '0.5', 'WEB': '0.375', 'ARXIV': '0.45', 'PASA': '0.5', 
                                'PKAS': '0.5', 'EUVE': '0.5', 'AGDP': '0.5', 'JAPA': '0.5', 'PASJ': '0.5', 'ASTL': '0.5', 'BLGAJ': '0.5', 
                                'PASP': '0.5', 'LPI': '0.5', 'IAU': '0.5', 'JAD': '0.5', 'JAA': '0.5', 'POBEO': '0.5', 'JPSJ': '0.5', 
                                'ARAC': '0.5', 'OAP': '0.5', 'NSTED': '0.5', 'A&G': '0.5', 'A&A': '0.5', 'PABEI': '0.5', 'APJ': '0.5', 
                                'QJRAS': '0.5', 'JAHH': '0.5', 'AAS': '0.5', 'APS': '0.5', 'ARA&A': '0.5', 'CFHT': '0.5', 'CXO': '0.5', 
                                'OEJV': '0.5', 'BEO': '0.5', 'ALMA': '0.5', 'TERRAPUB': '0.5', 'PADEU': '0.5', 'MOLDAVIA': '0.5', 'METBASE': '0.35', 
                                'GJI': '0.5', 'PAICz': '0.5', 'OCR': '0.3', 'A&AS': '0.5', 'STI': '0.375', 'HISSC': '0.5', 'SCI': '0.5', 
                                'SABER': '0.5', 'BASBR': '0.5', 'KNUDSEN': '0.35', 'PRINCETON': '0.4', 'IUE': '0.5', 'LIBRARY': '0.4', 
                                'AREPS': '0.5', 'CXC': '0.5', 'SERB': '0.5', 'ACASN': '0.5', 'PAICU': '0.5', 'OSA': '0.5', 'AMS': '0.5', 
                                'CHJAA': '0.5', 'PTP': '0.5', 'WGN': '0.5', 'ARIBIB': '0.45', 'SCIENCE': '0.5', 'KOBV': '0.5', 'PJAB': '0.5', 
                                'GCN': '0.5', 'GRG': '0.5', 'AAVSO': '0.5', 'SerAJ': '0.5', 'ASTRON': '0.5', 'SAO': '0.5', 'MPE': '0.5', 
                                'MPC': '0.5', 'PNAS': '0.5', 'STSci': '0.4', 'WILEY': '0.5', 'FCPH': '0.5', 'CBAT': '0.5', 'SPRN': '0.5', 
                                'JRASC': '0.5', 'LRR': '0.5', 'ASBIO': '0.5', 'T+F': '0.5', 'ACA': '0.5', 'CHAA': '0.5', 'CAPJ': '0.5', 
                                'UTAL': '0.4', 'NED': '0.25', 'PAOB': '0.5', 'SPIKA': '0.5', 'CHANDRA': '0.5', 'UMI': '0.5', 'AASP': '0.5', 
                                'ANRMS': '0.5', 'COPERNICUS': '0.5', 'ASP': '0.5', 'SPITZER': '0.5', 'ASPC': '0.5', 'CIEL': '0.5', 'LNP': '0.5', 
                                'M&PS': '0.5', 'COAST': '0.5', 'JST': '0.5', 'CUP': '0.5', 'ASD': '0.5', 'ANRFM': '0.5', 'MmSAI': '0.5', 'E&PSL': '0.5', 
                                'XMM': '0.5', 'NEWA': '0.5', 'ATSIR': '0.5', 'LRSP': '0.5', 'ATEL': '0.5', 'S&T': '0.5', 'PDS': '0.5', 'IMO': '0.5', 
                                'SIMBAD': '0.4', 'XTE': '0.5', 'FUSE': '0.5', 'USNO': '0.5', 'CARL': '0.4', 'SPIE': '0.5', 'COSKA': '0.5', 'OBS': '0.5', 
                                'GCPD': '0.35', 'PLR': '0.5', 'CDC': '0.5', 'CEAB': '0.5', 'JKAS': '0.5', 'WSPC': '0.5', 'EDP': '0.5', 'JIMO': '0.5', 
                                'ASL': '0.5', 'INGTN': '0.5', 'JHA': '0.5', 'LOC': '0.5', 'RVMA': '0.5', 'HOLLIS': '0.4', 'MNSSA': '0.5', 'KON': '0.5', 
                                'AAO': '0.5', 'M+PS': '0.5', 'STECF': '0.5', 'AIP': '0.5', 'ACTA': '0.5', 'JSTOR': '0.45', 'IAUC': '0.5', 'BALTA': '0.5', 
                                'BAVSR': '0.5', 'ADASS': '0.5', 'JENAM': '0.5', 'ADS': '0.5', 'DSSN': '0.5', 'KFNT': '0.5', 'SPRINGER': '0.5', 'ARNPS': '0.5', 
                                'JSARA': '0.5', 'ACHA': '0.5', 'UCP': '0.5', 'SF2A': '0.5', 'IAUDS': '0.5', 'NATURE': '0.5', 'ISSI': '0.5', 'POS': '0.4', 
                                'NRAO': '0.5', 'MNRAS': '0.5', 'BOTT': '0.5', 'STARD': '0.5', 'AFRSK': '0.5', 'PHYS': '0.5', 'O+T': '0.5', 'AG': '0.5', 
                                'ESP': '0.5', 'VERSITA': '0.5', 'AJ': '0.5', 'ICAR': '0.5', 'AN': '0.5', 'AP': '0.35', 'SLO': '0.5', 'ESA': '0.5', 
                                'ARI': '0.45', 'ESO': '0.5', 'BSSAS': '0.5', 'ICQ': '0.5', 'METIC': '0.5', 'ISAS': '0.5', 'KLUWER': '0.5', 'CSCI': '0.5', 
                                'BAAS': '0.5', 'CROSSREF': '0.35', 'CFA': '0.4', 'PSRD': '0.5', 'GONG': '0.35', 'BAAA': '0.5', 'IAJ': '0.5', 'AUTHOR': '0.5', 
                                'NCSA': '0.5', 'PHIJA': '0.5'}
}
