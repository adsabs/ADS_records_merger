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
@author: Giovanni Di Milia
File containing all the settings for the merger: priority lists and other
'''

from merger_functions import priority_based_merger, take_all, author_merger,\
    title_merger, abstract_merger

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

#If there is a specific priority list per one field its name should be specified here (see example)
#if not specified the standard one will be applied
FIELDS_PRIORITY_LIST = {
    #'doi' : 'doi_priority_list',
}

#priority lists
PRIORITY_LISTS = {
    'standard_priority_list' : []
}
