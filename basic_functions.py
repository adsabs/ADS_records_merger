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
File containing all the basic functions 
'''

import sys
import time

import merger_settings
from errors import OriginNotFound, OriginValueNotFound

def printmsg(verbose, msg):
    """function to print debug messages"""
    if verbose:
        sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S") + ' ' + msg)
        
def is_unicode(s):
    """function that checks if a string contains unicode or not"""
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return True
    else:
        return False

def is_mostly_uppercase(s):
    """function that checks if a string is mostly uppercase"""
    max_percentage = 80.0
    upper = 0 
    lower = 0
    for i in range(len(s)):
        if s[i].isupper():
            upper = upper + 1
        else:
            lower = lower + 1
    percentage = (float(upper) / len(s)) * 100
    if percentage > max_percentage:
        return True
    else:
        return False
    
def month_in_date(date):
    """function that checks if a date contains a valid month"""
    if len(date) == 7:
        month = date[0:2]
        if int(month) > 0 and int(month) < 13:
            return True
        else:
            return False
    else:
        return False

def get_origin(field):
    """function that extracts the origin of a field"""
    for subfield in field[0][0]:
        #for each subfield I search for the one containing the origin
        if subfield[0] == merger_settings.ORIGIN_SUBFIELD:
            return subfield[1]
        else:
            pass
    #if I don't find it I raise an exception
    raise OriginNotFound(str(field))

def get_origin_value(field, origins):
    """function that returns the value of the importace of an origin
    if multiple origin are present, the one with the highest value is returned"""
    #I split the string in a list of origins
    origin_list = origins.split('; ')
    #default value
    value = 0
    for origin in origin_list:
        #first of all I try to see if there is a specific list
        #otherwise I use the default one
        try:
            priority_list_name = merger_settings.FIELDS_PRIORITY_LIST[merger_settings.MARC_TO_FIELD[field]]
        except KeyError:
            priority_list_name = merger_settings.DEFAULT_PRIORITY_LIST
        
        priority_list = merger_settings.PRIORITY_LISTS[priority_list_name]

        try:
            cur_value = priority_list[origin]
        except KeyError:
            raise OriginValueNotFound('Priority value not found for origin "%s" %s' % (origin, str(origin_list)))
        
        if cur_value > value:
            value = cur_value
    return value

