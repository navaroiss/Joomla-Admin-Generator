import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.

import os, re

class SameAction:

    number_data_type = ['interger','int','tinyint','bigint','real','double','float']
    string_data_type = ['text','varchar','char','tinytext','longtext','mediumtext']
    time_date_type = ['time','date']
    content = ''

    trace = False
    trace_phase = []
    trace_type = 1

    php_version = 5
    template_path = result_path = ''
    slash = '/'
    ext = '.php'
    replate_data = {}

    def __init__(self):
        self.setTrace(True)

    def setTrace(self, value):
        self.trace = value
        self.trace_type = 2
        
    def printLog(self, msg, var):
        if self.trace is True:
            if self.trace_type == 2:
                print msg, var
            else:
                self.trace_phase.append(var)

    def makeFolder(self, folder_name):
        self.printLog("Creating folder ",folder_name)
        if(os.path.isdir(folder_name) is not True):
            os.makedirs(folder_name)

    def removeFolder(self, folder_name):
        self.printLog("Removing folder", folder_name)
        os.removedirs(folder_name)

    def readFile(self, file_path):
        self.printLog("Reading from file", file_path)
        f = open(file_path, "r")
        for i in f:
            print i

    def readTemplate(self, file_path):
        self.printLog("Reading from file", file_path)
        f = open(file_path, "r")
        text = ''
        for i in f:
            text += i
        return text
    
    def writeToFile(self, content, file_path):
        self.printLog("Writing to file", file_path)
        f = open(file_path, "w")
        f.write(content)
        f.close()

    def isFile(self, file_path):
        self.printLog("Checking file", file_path)
        return os.path.isfile(file_path)

    def isDir(self, path):
        return os.path.isdir(path)
    
    def pasrseTemplate(self, text):
        vars = re.findall("{\w+}", text)
        for var in vars:
            key = var[1:len(var)-1]
            if self.replate_data.has_key(key.lower()) or self.replate_data.has_key(key.upper()):
                value = self.replate_data[key]
            else:
                value = ""
            text = re.sub(var, value, text)
        return text

    def run(self):
        pass