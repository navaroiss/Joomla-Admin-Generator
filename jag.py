# To change this template, choose Tools | Templates
# and open the template in the editor.
# coding:utf8

__author__="Le Dinh Thuong-navaroiss"
__date__ ="$Jul 26, 2009 11:44:52 AM$"

import os, sys, os.path, shutil
from xml.dom import minidom
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-c', '--config', dest='config')
(options, args) = parser.parse_args()

from settings import *
from includes.controller import ActionController
from includes.model import ActionModel
from includes.view import ActionView
from includes.xmlpkg import Xmlpkg

def showAbout():
    """ Print somethings out """
    print
    print "=============================="
    print "| Joomla Admin Generator     |"
    print "| Le Dinh Thuong             |"
    print "| Version 1.0                |"
    print "=============================="
    print

def removeOldZip(file_path):
    """ Remove the zip file if it's living """
    if os.path.isfile(file_path) is True:
        os.remove(file_path)

def buildPackage(tables, table_fields):
    """ This is main script, this does anything we want """
    showAbout()
    
    if COMPONENT_NAME != '':
        RESULT_COMPONENT_PATH = os.path.join(RESULT_PATH, COMPONENT_NAME);
        if( os.path.isdir(RESULT_COMPONENT_PATH) is not True ):
            os.makedirs( RESULT_COMPONENT_PATH )

    removeOldZip( os.path.join(RESULT_COMPONENT_PATH, COMPONENT_NAME + '.zip') )

    """ This setting will be put into some classes """
    settings = {
        'template_path':TEMPLATE_PATH,
        'template_controller':TEMPLATE_CONTROLLER,
        'result_path':RESULT_COMPONENT_PATH,
        'php_version':PHP_VERSION,
        'component_name':COMPONENT_NAME,
        'template_model':TEMPLATE_MODEL,
        'author_name':AUTHOR_NAME,
        'author_email':AUTHOR_EMAIL,
        'php_date_time':PHP_DATE_TIME
    }

    """Create model"""
    ActionModel( table_fields, settings )
    """Create contrller"""
    ActionController( tables, table_fields, settings )
    """Create view"""
    ActionView( tables, table_fields, settings )
    
    """ Copy folder assets from template to result path if it's directory"""
    if os.path.isdir(RESULT_COMPONENT_PATH+"/assets") is False:
        shutil.copytree(TEMPLATE_PATH+"/assets", RESULT_COMPONENT_PATH+"/assets")

    Xmlpkg(tables, settings)

""" 
We fetch the value of attributes from xml and call function buldPackage() to do all things.
Use xml.dom.minidom class we have some methods below:
minidom.parse(xml_file_path)
....getElementsByTagName()
....getAttribute()
"""
if hasattr(options, 'config') and options.config != None:
    """ List table name and sort name """
    tables = []
    fields = []
    file_xml_config = os.path.join(os.path.dirname(__file__), options.config)
    xml_parser = minidom.parse(file_xml_config)
    try:
        for table in xml_parser.getElementsByTagName('table'):
            tables.append( [ table.getAttribute('sort_name') , table.getAttribute('name')] )
            data = []
            for field in table.getElementsByTagName('field'):
                type = []
                
                if field.getAttribute('type') == 'int':
                    """ Integer """
                    s = "%s(%s)" % ( field.getAttribute('type'), field.getAttribute('length') )
                    type.append( s )
                    if field.getAttribute('auto_increment').lower() == "true":
                        type.append('auto_increment')
                    if field.getAttribute('primary_key').lower() == 'true':
                        pass
                    if len(field.getAttribute('belong').lower()) > 0:
                        type.pop()
                        type.append( 'tree' )
                        type.append(table.getAttribute('name'))
                        type.append('name')
                        type.append(field.getAttribute('belong'))
                        type.append(field.childNodes[0].data)
                
                elif field.getAttribute('type') == 'varchar':
                    """ Varchar """
                    s = "%s(%s)" % ( field.getAttribute('type'), field.getAttribute('length') )
                    type.append( s )
                    
                elif field.getAttribute('type') == 'text':
                    """ Text """
                    type.append( field.getAttribute('type') )
                
                elif field.getAttribute('type') == 'date':
                    """ Date """
                    type.append( field.getAttribute('type') )
                    type.append( field.getAttribute('design') )
                    
                elif field.getAttribute('type') == 'file': 
                    """ File """
                    type.append( field.getAttribute('type') )
                    type.append( field.getAttribute('file_type').split(',') )
                
                elif field.getAttribute('type') == 'tree':
                    """ Tree """
                    type.append( field.getAttribute('type') )
                    type.append( field.getAttribute('table_name') )
                    type.append( field.getAttribute('table_field_name') )
                    type.append( field.getAttribute('table_field_primary') )
                    type.append( field.getAttribute('table_field_parent') )
                
                elif field.getAttribute('type') == 'listfile':
                    """ Listfile """
                    type.append( field.getAttribute('type') )
                    type.append( field.getAttribute('folder'))
                    
                elif field.getAttribute('type') == 'boolean':
                    """ Boolean """
                    type.append( field.getAttribute('type') )
                
                """ Add the field to dict """
                data.append( {field.childNodes[0].data:type} )
            """ Add the dict, that consits the table name and the field """
            fields.append( {table.getAttribute('name'):data} )
        
        """ Setting global variables """
        COMPONENT_NAME = xml_parser.firstChild.getAttribute('name').encode('ascii')
        AUTHOR_NAME = xml_parser.firstChild.getAttribute('author').encode('ascii')
        AUTHOR_EMAIL = xml_parser.firstChild.getAttribute('email').encode('ascii')
    except AttributeError:
        pass
    
    """ Call the main function """
    buildPackage(tables, fields)
