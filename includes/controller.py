# To change this template, choose Tools | Templates
# and open the template in the editor.

from action import *
from time import gmtime, strftime

class ActionController(SameAction):
    """ Class ActionController """
    
    template_controller = ''
    def __init__(self, tables, table_fields, config={}):
        
        self.template_path = config['template_path']
        self.template_controller = config['template_controller']
        self.result_path = config['result_path']
        self.php_version = config['php_version']
        self.component_name = config['component_name']
                
        self.replate_data['AUTHOR_NAME'] = config['author_name']
        self.replate_data['AUTHOR_EMAIL'] = config['author_email']
        self.replate_data['COMPONENT_PATH'] = self.component_name

        """ Use Controller_Interface in php if php_version > 5 """
        if self.php_version>=5:
            self.includeInterface()
        
        i = 0
        for fields in table_fields:
            controller_name = tables[i][0]
            table_name = tables[i][1]
            self.replate_data['CONTROLLER_NAME'] = controller_name.capitalize()
            self.replate_data['TABLE_NAME'] = table_name
            self.replate_data['VAR'] = controller_name;
            self.replate_data['PRI_KEY'] = 'id'
            self.replate_data['FILE_NAME'] = controller_name + self.ext
            self.replate_data['TIME'] = strftime("%a, %d %b %Y %H:%M:%S", gmtime())                
            self.run(fields, controller_name)
            i = i + 1
    
    def filterQuery(self, fields):
        self.replate_data['JOIN_QUERY'] = ''
        self.replate_data['CONDITION']  = ''
        join_query = condition = ''
        string_type = []
        table_name = fields.keys()[0]
        for field in fields.values()[0]:
            field_name = field.keys()[0]
            field_type = field[field_name][0]
            if field_type  == 'tree':
                first_table = field[field_name][1]
                first_field = field[field_name][3]
                join_query = "if( count($_POST)>=1 ){\n"
                join_query += "if($_POST[$this->var]['%s']>=1){\n" % (field_name)
                join_query += "        $value = $_POST[$this->var]['%s'];" % (field_name)
                join_query += '        $join_query[\'select\']  = "a.*"; \n'
                join_query += '        $join_query[\'table\']  = "#__%s a";\n' % (first_table)
                if field[field_name][1] == table_name:
                    join_query += '        $join_query[\'condition\']  = "a.%s=#__%s.%s and a.%s = $value";}}'%(field_name, first_table, first_field, field_name)
                else:
                    join_query += '        $join_query[\'condition\']  = "#__%s.%s=a.%s and #__%s.%s = $value";}}'%(table_name, field_name, first_field, table_name, field_name)
            elif self.string_data_type.count(field_type) >= 1:
                """condition = "if(count($_POST)>=1){\n"
                condition += " if($_POST[$this->var]['%s']>=1) $condition['%s'] = $_POST[$this->var]['%s'];" % (field_name, field_name, field_name)
                condition += "}"""
                s = "`%s` like '%s$keywords%s'" % (field_name, '%', '%')
                string_type.append(s)
            
        if join_query != '':
            self.replate_data['JOIN_QUERY'] = join_query
        if len(string_type) >= 1:
            self.replate_data['CONDITION'] = "if ($keywords!='') $find_keyword = \"%s\";\n" % (' or '.join(string_type))
        self.replate_data['CONDITION'] += condition
        
    def fileAllow(self, fields):
        """ Add php code to upload file depend on the setting of field """
        php_file_allow = ''
        self.replate_data['FILE_EXT_ALLOW']  = ''
        for field in fields.values()[0]:
            field_name = field.keys()[0]
            field_type = field[field_name][0]
            if field_type == 'file':
                if len( field[field_name][1] ) == 1:
                    allow_type = field[field_name][1][0]
                    if allow_type=="image":
                        php_file_allow += "\t\t$file_ext_allow['%s'] = $this->_ext['image'];\n" % (field_name)
                    elif allow_type=="video":
                        php_file_allow += "\t\t$file_ext_allow['%s'] = $this->_ext['video'];\n" % (field_name)
                    elif allow_type=="audio":
                        php_file_allow += "\t\t$file_ext_allow['%s'] = $this->_ext['audio'];\n" % (field_name)
                    elif allow_type=="document":
                        php_file_allow += "\t\t$file_ext_allow['%s'] = $this->_ext['document'];\n" % (field_name)
                    elif allow_type=="compress":
                        php_file_allow += "\t\t$file_ext_allow['%s'] = $this->_ext['compress'];\n" % (field_name)
                    elif allow_type=="application":
                        php_file_allow += "\t\t$file_ext_allow['%s'] = $this->_ext['application'];\n" % (field_name)
                    else:
                        php_file_allow += "$_all=array();"
                        php_file_allow += "\t\tforeach($this->_ext as $k=>$v){ $_all = array_merge($_all, $v); } $file_ext_allow['%s'] = $_all;\n" % (field_name)
                elif len( field[field_name][1] ) > 1:
                    c = []
                    for it in field[field_name][1]:
                        c.append("$k == '%s'" % (it.strip()))
                    upload_cond = ' or '.join(c)
                    php_file_allow += "$_some=array();"
                    php_file_allow += "foreach($this->_ext as $k=>$v){ if (%s) $_some = array_merge($_some, $v); }" % (upload_cond)
                    php_file_allow += " $file_ext_allow['%s'] = $_some;" % (field_name)
            
        self.replate_data['FILE_EXT_ALLOW'] = php_file_allow

    
    def includeInterface(self):
        include_interface = "include_once( dirname(__FILE__).DS.'interface.php' );"
        implement_interface = "implements Controller_Interface"
        
        self.replate_data['INCLUDE_INTERFACE'] = include_interface
        self.replate_data['IMPLEMENT_INTERFACE'] = implement_interface
        result_controller_path = self.result_path + self.slash + "controllers" + self.slash
        interface_file = result_controller_path+self.slash+'interface'+self.ext
        
        if self.isFile(interface_file) is not True:
            interface_text = self.readTemplate(self.template_controller + self.slash + "interface"+self.ext)
            if self.isDir(result_controller_path) is False:
                self.makeFolder(result_controller_path)
            self.writeToFile(interface_text, interface_file)

    def run(self, fields, controller_name):
        """ Call the method to write php code """
        self.filterQuery(fields)   
        self.fileAllow(fields)

        """ Split component name """
        com = com_name = ''
        try:
            com, com_name = self.component_name.split('_')
        except ValueError:
            pass
        text = ''
        """ Read template from controller.php """
        text = self.readTemplate(self.template_controller + self.slash + "controller"+self.ext)
        """ Make folder """
        result_controller_path = self.result_path + self.slash + "controllers" + self.slash
        self.makeFolder(result_controller_path)
        """ Read and write the interface """
        file_path = self.template_controller + self.slash + 'interface' + self.ext
        interface_text = self.readTemplate(file_path)
        file_path = self.result_path + self.slash + "controllers" + self.slash + 'interface' + self.ext
        self.writeToFile(interface_text, file_path)
        """ """
        if self.isFile(result_controller_path+com_name+self.ext) is not True:
            root_content = self.readTemplate(self.template_controller + self.slash + "root_controller"+self.ext)
            self.writeToFile(root_content, self.result_path+self.slash+com_name+self.ext)

        text = self.pasrseTemplate(text)
        self.writeToFile(text, result_controller_path+ controller_name.lower()+ self.ext)
