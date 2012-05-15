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
Main module

It parses the parameters and calls the global manager
'''

from optparse import OptionParser
import sys
if sys.version_info < (2, 6):
    raise "Must use python 2.6 or greater"

import pipeline_manager

def parse_parameters():
    """Function that parse the parameters passed to the script"""
    parser = OptionParser()

    parser.add_option("-m", "--mode", dest="mode", help="Specify the method of extraction (\"full\" or \"update\") ", metavar="MODEVALUE")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help='Use this parameter if a verbose execution is needed ')

    # catch the parameters from the command line
    options, _ = parser.parse_args()

    #Dictionary to return parameters
    parameters = {}

    if options.mode:
        if options.mode == 'full' or options.mode == 'update':
            parameters['mode'] = options.mode
        else:
            parser.print_help()
            return None
    else:
        parser.print_help()
        return None

    if options.verbose:
        parameters['verbose'] = True
    else:
        parameters['verbose'] = False

    return parameters

def main():
    """ Main Function"""
    #Manage parameters
    parameters = parse_parameters()
    if parameters == None:
        return
    #I call the global manager
    pipeline_manager.manage(parameters['mode'], parameters['verbose'])

if __name__ == "__main__":
    main()
