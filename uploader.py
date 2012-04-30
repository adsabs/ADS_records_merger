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
A custom version of the invenio bibupload module 
to upload directly in the Invenio DB the result of the merger
'''
import sys
from invenio import bibupload
from merger_settings import VERBOSE, msg as msg_func

def write_message(msg, stream=sys.stdout, verbose=VERBOSE):
    """Custom definition of write_message 
    to override the Invenio log"""
    msg_func(msg, verbose)

bibupload.write_message = write_message

def bibupload_merger(merged_bibrecords, pretend=False, verbose=VERBOSE):
    """Function to upload directly in the Invenio DB"""
    
    for bibrecord in merged_bibrecords:
        bibupload.bibupload(bibrecord, opt_tag=None, opt_mode="replace_or_insert",
                  opt_stage_to_start_from=1, opt_notimechange=0, oai_rec_id = "", pretend=pretend)