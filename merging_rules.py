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
File containing all the functions to merge 
'''

from basic_functions import get_origin, get_origin_value, printmsg
from settings import VERBOSE

def priority_based_merger(subfield_list1, subfield_list2, field_code):
    """basic function that merges based on priority"""
    
    origin_val1 = get_origin_value(field_code, get_origin(subfield_list1))
    origin_val2 = get_origin_value(field_code, get_origin(subfield_list2))
    
    if origin_val1 > origin_val2:
        return subfield_list1
    elif origin_val2 > origin_val1:
        return subfield_list2
    else:
        #in case the two values are the same, I return the first one and I print a worning
        #warning
        printmsg(VERBOSE, 'Same field with origin having the same importance.')
        return subfield_list1
    
def take_all(subfield_list1, subfield_list2, field_code):
    """function that takes all the different fields 
    and returns an unique list"""
    
def author_merger(subfield_list1, subfield_list2, field_code):
    """function that merges the author lists and return the first author or
     all the other authors"""
     
def title_merger(subfield_list1, subfield_list2, field_code):
    """function that chooses the titles and returns the main title or 
    the list of alternate titles"""
    
def abstract_merger(subfield_list1, subfield_list2, field_code):
    """function that chooses the abstracts based on the languages and priority"""
    
    



