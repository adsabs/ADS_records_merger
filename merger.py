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
The ads merger is a tool that combines two elements and returns 
the combined element.
'''

import merger_settings

def merger(record):
    """Main function: takes in input a whole record containing the 
    different flavors of metadata"""
    
    
def merge_field(field1, field2, field_type):
    """Function that merges two fields based on the field type"""

    #I retrieve the merging function (that is a representation of the merging rule) for the specified field
    merging_func = merger_settings.MERGING_RULES[merger_settings.MARC_TO_FIELD[field_type]]
    #I apply the merging rule
    return merging_func(field1, field2)