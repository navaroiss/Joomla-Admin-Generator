import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.

from includes.action import SameAction
from time import strftime, gmtime
import os, shutil, zipfile

class Xmlpkg(SameAction):

    def __init__(self, tables, config):
        folder = file = ""
        listfiles = self.listDir( config['result_path'], {'folder':[], 'file':[]} )
        for fi in listfiles['file']:
            name = fi.replace(config['result_path']+self.slash, '')
            file += "<filename>"+name+"</filename>\n"
        self.replate_data['FOLDER'] = folder
        self.replate_data['FILE'] = file

        file_path = config['template_path'] + self.slash + 'package.xml'
        xml = self.readTemplate(file_path)

        self.replate_data['DATE'] = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        self.replate_data['AUTHOR_NAME'] = config['author_name']
        self.replate_data['AUTHOR_EMAIL'] = config['author_email']
        self.replate_data['COMPONENT_PATH'] = config['component_name']

        com = name = ''
        try:
            com,name = config['component_name'].split('_')
        except ValueError:
            pass
        self.replate_data['COMPONENT_NAME'] = name.capitalize()

        if len(tables)>1:
            submenu = ''
            for sm in tables:
                submenu += '<menu link="option=%s&amp;c=%s" img="js/ThemeOffice/component.png">%s</menu>\n' % (config['component_name'], sm[0], sm[0].capitalize())
            self.replate_data['SUBMENU'] = '<submenu>'+ submenu +'</submenu>'

        xml = self.pasrseTemplate(xml)
        if os.path.isdir(config['result_path']):
            #xml_file_path = os.path.dirname(config['result_path']) + self.slash + name + '.xml'
            xml_file_path = config['result_path'] + self.slash + name + '.xml'
        self.writeToFile(xml, xml_file_path)

        self.createPakage(config['component_name'], config['result_path'])
        
    def listDir(self, root_path, result):
        folder = result['folder']
        file = result['file']
        for item in os.listdir(root_path):
            path = os.path.join(root_path, item)
            if os.path.isdir(path):
                folder.append(path)
                result = {'folder':folder, 'file':file}
                self.listDir(path, result)
            else:
                file.append(path)
        result = {'folder':folder, 'file':file}
        return result

    def zipfolder(self, path, relname, archive, basefolder = ''):
        paths = os.listdir(path)
        if len(paths)>=1:
            for p in paths:
                p1 = os.path.join(path, p)
                p2 = os.path.join(relname, p)
                print "Added: %s" % (p1)
                if os.path.isdir(p1):
                    self.zipfolder(p1, p2, archive)
                else:
                    try:
                        fext = p1.split('.')[-1]
                        if fext != 'zip':
                            archive.write(p1, p2)
                        else:
                            pass
                    except ValueError:
                        pass
        else:
            print "Added: %s" % (path)
            archive.write(path)

    def createPakage(self, package, path):
        #if os.path.isdir(path):
        #    path = os.path.dirname(path)
        """
        cmd = "cd %s && zip -r %s ./" % (path, package)
        os.system(cmd)
        print "Package: %s/%s.zip" % (path, package)
        """
        compressedFile = zipfile.ZipFile("%s.zip"%(os.path.join(path,package)),"w", zipfile.ZIP_STORED)
        self.zipfolder(os.path.join(path), "/", compressedFile, os.path.join(path))
        if os.path.isfile("%s.zip"%(os.path.join(path,package))):
            print "The component was successfuly compressed in %s.zip" % (os.path.join(path,package))
            
