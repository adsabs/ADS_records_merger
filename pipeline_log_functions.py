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
File containing global functions
'''

import sys
import os
import time

from pipeline_settings import VERBOSE

def msg(message, verbose=VERBOSE):
    """
    Prints a debug message.
    """
    if verbose:
        print time.strftime("%Y-%m-%d %H:%M:%S"), '---', message


def manage_check_error(msg_str, type_check):
    """function that prints a warning or 
    raises an exception according to the type of check"""
    
    from merger.merger_errors import GenericError
    
    if type_check == 'warnings':
        msg('          CHECK WARNING: %s' % msg_str , True)
    elif type_check == 'errors':
        raise GenericError(msg_str)
    else:
        raise GenericError('Type of check "%s" cannot be handled by the "manage_check_error" function.')
    return None