# To change this template, choose Tools | Templates
# and open the template in the editor.

from action import *
import re
from time import gmtime, strftime


class ActionModel(SameAction):
        
    def __init__(self, table_fields, config={}):

        self.template_path = config['template_path']
        self.template_model = config['template_model']
        self.result_path = config['result_path']
        self.php_version = config['php_version']
        self.component_name = config['component_name']

        self.table_fields = table_fields
        self.parent = 1000 # Nang cap o phien ban sau
        com = name = ''
        try:
            com, name = self.component_name.split('_')
        except ValueError:
            pass

        self.replate_data['COMPONENT_NAME'] = name.capitalize()
        self.replate_data['AUTHOR_NAME'] = config['author_name']
        self.replate_data['AUTHOR_EMAIL'] = config['author_email']
        self.replate_data['COMPONENT_PATH'] = self.component_name
        self.replate_data['TIME'] = strftime("%a, %d %b %Y %H:%M:%S", gmtime())

        self.run()

    def run(self):

        self.generateSQL()

        file_path = self.template_model + self.slash + 'model' + self.ext
        text = self.readTemplate(file_path)
        self.replate_data['FILE_NAME'] = 'models' + self.ext
        text = self.pasrseTemplate(text)
        result_model_path = self.result_path + self.slash + 'models'
        self.makeFolder(result_model_path)
        self.writeToFile(text, result_model_path + self.slash + 'models' + self.ext)
        
        file_path = self.template_model + self.slash + 'helper' + self.ext
        text = self.readTemplate(file_path)
        self.replate_data['FILE_NAME'] = 'helper' + self.ext
        text = self.pasrseTemplate(text)
        self.writeToFile(text, result_model_path + self.slash + 'helper' + self.ext)
        

    def generateSQL(self):
        dropSQL = self.DropSQL()
        sql = ''
        for q in dropSQL:
            sql += "\n" + q
        self.replate_data['DROPQUERIES'] = sql
        file_uninstall = 'uninstall.%s' % (self.component_name)
        file_path = self.template_path + self.slash + 'uninstall' + self.ext
        self.replate_data['FILE_NAME'] = file_uninstall + self.ext
        text = self.pasrseTemplate(self.readTemplate(file_path))
        file_path = (self.result_path + self.slash + file_uninstall + self.ext)
        self.writeToFile(text, file_path)

        createSQL = self.CreateSQL()
        sql = ''
        for q in createSQL:
            sql += "\n" + q
        self.replate_data['CREATEQUERIES'] = sql
        file_install = 'install.%s' % (self.component_name)
        file_path = self.template_path + self.slash + 'install' + self.ext
        self.replate_data['FILE_NAME'] = file_install + self.ext
        text = self.pasrseTemplate(self.readTemplate(file_path))
        file_path = (self.result_path + self.slash + file_install + self.ext)
        self.writeToFile(text, file_path)


    def DropSQL(self):
        SQL = []
        for table in self.table_fields:
            query = "$installQueries[] = 'DROP TABLE `#__%s`';" % (table.keys()[0])
            SQL.append(query)
        return SQL

    def CreateSQL(self):
        SQL = []
        for table in self.table_fields:
            query = "$installQueries[] = 'DROP TABLE IF EXISTS `#__%s`';" % (table.keys()[0])
            SQL.append(query)
            query = "$installQueries[] = 'CREATE TABLE `#__%s` (" % (table.keys()[0])
            PRI_KEY = ''
            for field in table[table.keys()[0]]:
                query += " `%s` " % (field.keys()[0])
                for type in field[field.keys()[0]]:
                    if type == "auto_increment":
                        PRI_KEY = "PRIMARY KEY  (`%s`)" % (field.keys()[0])
                    c_type = field[field.keys()[0]][0]
                    if c_type =='tree':
                        if type == c_type:
                            query += " int(11)"
                        continue
                    elif c_type =='file':
                        if type == c_type:
                            query += " varchar(255)"
                        continue
                    elif c_type == "listfile":
                        if type == c_type:
                            query += " varchar(255)"
                        continue
                    elif c_type == 'date':
                        if type == c_type:
                            query += " date"
                        continue
                    elif c_type == 'tree':
                        if type == c_type:
                            query += " int(11)"
                        continue
                    else:
                        query += " %s" % (type)
                query += ","
            query += PRI_KEY + ")ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8';"
            SQL.append(query)
            
            
            #SQL += "\n insert into #__components(`name`,`link`,`parent`,`admin_menu_link`,`admin_menu_alt`,`option`,`params`,`admin_menu_img`)"
            #name = self.searchKey(table)
            #SQL += " values('%s','option=%s', %s, 'option=%s&c=%s', '%s', '%s',' ','js/ThemeOffice/component.png')" % (name.capitalize(), self.component_name, self.parent, self.component_name, name, name, self.component_name)
            #SQL += ";\n"
        return SQL

    def searchKey(self, value):
        for k,v in self.tables.items():
            if v == value:
                return k
            