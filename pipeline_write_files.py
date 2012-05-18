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
Module that manages the writing of files
It has been created to be sure that the resources allocated for this operation
can be freed just after the operation is complete
'''

import os
import inspect

import pipeline_settings as settings
from pipeline_log_functions import msg as printmsg
from merger.merger_errors import GenericError

class WriteFile(object):
    """Class that writes the output files of the pipeline"""

    def __init__(self, dirname, logger):
        """Constructor"""
        #I set the directory where to write
        self.dirname = dirname
        self.logger = logger

    def write_done_bibcodes_to_file(self, bibcodes_list):
        """Method that writes a list of bibcodes in the file of the done bibcodes"""
        self.logger.info("In function %s.%s" % (self.__class__.__name__, inspect.stack()[0][3]))

        filepath = os.path.join(settings.BASE_OUTPUT_PATH, self.dirname, settings.BASE_FILES['done'])

        try:
            file_obj = open(filepath, 'a')
            for bibcode in bibcodes_list:
                file_obj.write(bibcode+'\n')
            file_obj.close()
        except:
            err_msg = 'Impossible to write in the "bibcode done file" %s \n' % filepath
            self.logger.critical(err_msg)
            raise GenericError(err_msg)
        return True

    def write_problem_bibcodes_to_file(self, bibcodes_list):
        """Method that writes a list of bibcodes in the file of the done bibcodes"""
        self.logger.info("In function %s.%s" % (self.__class__.__name__, inspect.stack()[0][3]))
        
        filepath = os.path.join(settings.BASE_OUTPUT_PATH, self.dirname, settings.BASE_FILES['prob'])
        
        try:
            file_obj = open(filepath, 'a')
        except:
            err_msg = 'ERROR: impossible to open the "bibcode problematic file" %s \n' % filepath
            self.logger.critical(err_msg)
            raise GenericError(err_msg)
            
        for bibcode, failing_reason in bibcodes_list:
            try:
                str_to_print = bibcode + '\t'+ failing_reason + '\n'
                file_obj.write(str_to_print)
            except:
                try:
                    str_to_print = u'%s\t%s\n' % (unicode(bibcode), failing_reason)
                    file_obj.write(str_to_print.encode('UTF-8'))
                except:
                    err_msg = 'ERROR: impossible to write in the error of %s in "bibcode problematic file" %s \n' % (bibcode, filepath)
                    self.logger.critical(err_msg)
                    raise GenericError()
        file_obj.close()
        return True

