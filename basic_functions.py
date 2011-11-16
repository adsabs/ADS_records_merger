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
File containing all the basic functions 
'''

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