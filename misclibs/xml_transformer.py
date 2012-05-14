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

""" Class that define an engine for XSLT transformations

"""

#libraries to transform the xml
import libxml2
import libxslt
import inspect 

import pipeline_settings as settings
from pipeline_log_functions import msg as printmsg
from merger.merger_errors import GenericError

class XmlTransformer(object):
    """ Class that transform an ADS xml in MarcXML"""
        
    def __init__(self, verbose):
        """ Constructor"""
        self.verbose = verbose
        #definition of the stilesheet
        self.stylesheet = settings.STYLESHEET_PATH
        #I initialize the style sheet object
        self.style_obj = None
    
    def init_stylesheet(self):
        """ Method that initialize the transformation engine """
        printmsg("In function %s.%s" % (self.__class__.__name__, inspect.stack()[0][3]), self.verbose)
        #create the stylesheet obj
        try:
            self.style_obj = libxslt.parseStylesheetDoc(libxml2.parseFile(self.stylesheet))
        except:
            raise GenericError("ERROR: problem loading stylesheet \n")
        
        return True
    
    def transform(self, doc):
        """ Method that actually make the transformation"""
        printmsg("In function %s.%s" % (self.__class__.__name__, inspect.stack()[0][3]), self.verbose)
        
        #I load the stylesheet
        self.init_stylesheet()
                
        #transformation
        try:
            doc = self.style_obj.applyStylesheet(doc, None)
        except:
            printmsg("ERROR: Transformation failed", True) 
            return False
        
        #to string
        result = self.style_obj.saveResultToString(doc)
        
        #self.styleObj.freeStylesheet()
        doc.freeDoc()
        
        return result
    

def create_record_from_libxml_obj(domdoc):
    """Creates a record from the document (of type libxml2/libxslt)."""
    #I define some names for the tags before getting to the actual marcxml
    global_wrapper = 'collections'
    record_wrapper = 'collection'
    record_version_wrapper = 'record'
    
    #I define an XPATH handler
    ctxt = domdoc.xpathNewContext()
    #I select all the records (that are defined by the "collection" tag (maybe it's better to raname these tags in something like collection/record/recordversion to avoid misunderstanding)
    retrieved_records = ctxt.xpathEval('/%s/%s'%(global_wrapper, record_wrapper))
    #If I haven't found any record I return an empty bibrecord
    if len(retrieved_records) == 0:
        return {}
    #else:
    #    print 'found %s records' % len(retrieved_records)
    
    #global list for the records I retrieve
    all_bibrecords = []
        
    #If I have records, I process each record and then each version of the record
    for retrieved_record in retrieved_records:
        #list for the versions of the record I find
        bibrecord_versions = []
        #I set the context node to the current one
        ctxt.setContextNode(retrieved_record)
        record_versions = ctxt.xpathEval(record_version_wrapper)
        #if I have no record versions it's an empty instance so I can skip it
        if len(record_versions) == 0:
            continue
        #otherwise I start to analize the single record version
        for record_version in record_versions:
            #I define a global counter  and the wrapper for all the record
            field_position_global = 1
            bibrecord_version = {}
            
            ctxt.setContextNode(record_version)
            datafields = ctxt.xpathEval('datafield')
            #if I don't have any datafield it means that the record is empty and I can skip it
            if len(datafields) == 0:
                continue
            #otherwise I can parse the datafields
            for datafield in datafields:
                ctxt.setContextNode(datafield)
                #I extract infos at the datafield level
                try:
                    tag = ctxt.xpathEval('@tag')[0].content#.encode('utf-8')
                    ind1 = ctxt.xpathEval('@ind1')[0].content#.encode('utf-8')
                    ind2 = ctxt.xpathEval('@ind2')[0].content#.encode('utf-8')
                except IndexError:
                    #if something is missing from the XML I skip the field
                    continue
                #I sanitaze the indicators
                if ind1 == '':
                    ind1 = ' '
                if ind2 == '':
                    ind2 = ' '
                #I extract the subfields
                subfields = ctxt.xpathEval('subfield')
                if len(subfields) == 0:
                    continue
                #I define a list where to store the subfields
                bibrecord_subfields = []
                for subfield in subfields:
                    value = subfield.content#.encode('utf-8')
                    ctxt.setContextNode(subfield)
                    try:
                        code = ctxt.xpathEval('@code')[0].content.encode('utf-8')
                    except IndexError:
                        continue
                    #then I put the result inside the list of subfields
                    bibrecord_subfields.append((code, value,))
                #then I append the field to the main record
                bibrecord_version.setdefault(tag, []).append((bibrecord_subfields, ind1, ind2, '', field_position_global,))
                field_position_global += 1
            #then I append the bibrecord version to the list of all the versions for this record
            bibrecord_versions.append(bibrecord_version)
        #finally I append all the versions of the same record to the list of records
        all_bibrecords.append(bibrecord_versions)
    
    return all_bibrecords
    