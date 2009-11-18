# To change this template, choose Tools | Templates
# and open the template in the editor.

from action import *
from time import gmtime, strftime

class ActionView(SameAction):
    
    table_name = ''
    table = table_fields = ''

    td_row_editor = '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >\n<?php echo $editor->display("%s[%s]",(isset($row->%s)?$row->%s:""), "550", "150", "60", "10", array("readmore") );?>\n</td>\n</tr>\n';
    td_row = '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >\n<input class="inputbox" type="text" name="%s[%s]" id="%s" size="60" maxlength="255" value="<?php if($edit==true) echo $row->%s; ?>" />\n</td>\n</tr>\n';
    td_col_name = '<th class="title">%s</th>\n'
    td_col_value = '<td><?php echo substr(strip_tags($v->%s), 0, 150)?></td>\n'
    
    def __init__(self, tables, table_fields, config={}):
        self.php_date_time = config['php_date_time']
        self.template_path = config['template_path']
        self.template_controller = config['template_controller']
        self.result_path = config['result_path']
        self.php_version = config['php_version']
        self.component_name = config['component_name']

        self.replate_data['AUTHOR_NAME'] = config['author_name']
        self.replate_data['AUTHOR_EMAIL'] = config['author_email']
        self.replate_data['COMPONENT_PATH'] = self.component_name

        i = 0
        for table in table_fields:
            controller_name = tables[i][0]
            table_name = tables[i][1]            
            self.var = controller_name
            self.table_name = table_name 
            self.replate_data['FILE_NAME'] = 'admin.'+self.var+'.html' + self.ext
            self.replate_data['TIME'] = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
            self.replate_data['FILTER'] = ''            
            self.run(table, table_name)
            i = i + 1

    def run(self, table, table_name):
        self.generateForm(table, table_name)
        self.generateTable(table, table_name)
        
        file_path = self.template_path + self.slash + 'views' + self.slash + 'view' + self.ext
        text = self.readTemplate(file_path)
        result_view_path = self.result_path + self.slash + 'views'
        self.makeFolder(result_view_path)
        """
        try:
            if len(self.replate_data['FILTER']) > 1:
                use_filter = False
                for field in self.table:
                    for type in self.table[field]:
                        if type.split(':')[0] == 'tree':
                            use_filter = True
                            break
                if use_filter == False:
                    self.replate_data['FILTER'] = ''
        except KeyError:
            pass
        """
        for field in table[table_name]:
            field_name = field.keys()[0]
            field_type = field[field_name][0]
            if field_type == 'tree':
                js = "onchange='document.adminForm.submit();'"
                self.replate_data['FILTER'] = '<?php $field["field_name"]="%s[%s]"; $field["id"]="%s"; $field["name"]="%s"; $field["parent"]="%s"?>\n' % (self.var, field_name, field[field_name][3], field[field_name][2], field[field_name][4])
                self.replate_data['FILTER'] += '<?php echo listCategories((count($_POST)>=1?$_POST["%s"]["%s"]:0), %s, "%s", "%s");?>' % (self.var, field_name, '$field', field[field_name][1], js)

        text = self.pasrseTemplate(text)
        file_path = result_view_path + self.slash + 'admin.'+self.var+'.html' + self.ext
        self.writeToFile(text, file_path)

    def generateForm(self, table, table_name):
        form_html = ''
        self.replate_data['FORM_FIELDS'] = ''
        for field in table[table_name]:
            field_name = field.keys()[0]
            field_type = field[field_name][0]
            if field_type == 'text':
                self.replate_data['GET_EDITOR'] = '$editor =& JFactory::getEditor();';
                form_html += self.td_row_editor % (field_name, field_name.capitalize(),self.var,  field_name, field_name,field_name)
            elif field_type == "boolean":
                form_html += self.autoBooleanField(field_type, field_type)
            elif field_type == "date":
                form_html += self.autoDateField(field_name, field_type)
            elif field_type == "listfile":
                form_html += self.autoListField(field_name, field_type)
            elif field_type == 'file':
                form_html += self.autoFileField(field_name, field_type)
            elif field_type == 'tree':
                form_html += self.autoTreeField(field, field_name)
            elif 'int' in field_type:
                try:
                    if field[field_name][1] == 'auto_increment':
                        form_html += ''
                    if len(field[field_name]) == 4:
                        form_html += self.autoTreeField(field, field_name)
                except IndexError:
                    pass
            else:
                form_html += self.td_row % (field_name, field_name.capitalize(),self.var,field_name,field_name,field_name)
        self.replate_data['FORM_FIELDS'] = form_html

    def generateTable(self, table, table_name):
        table_field_name = table_field_value =''
        field_show = []
        field_key = ''
        for field in table[table_name]:
             field_name = field.keys()[0]
             field_type = field[field_name][0]
             if self.isFString(field_type):
                field_show.append(field_name)
             if "auto_increment" in field[field_name]:
                field_key = field_name
        if len(field_show)>=1:
            for item in field_show:
                table_field_name += self.td_col_name % (item.capitalize())
                table_field_value += self.td_col_value % (item)
                
        table_field_name += self.td_col_name % ("Action")
        table_field_value += "<td width='10'><a href='index.php?option=%s&c=%s&task=edit&id=<?=$v->%s?>'><img src='components/%s/assets/images/edit.png'/></a></td>\n" % (self.component_name, self.var, field_key, self.component_name)
        
        self.replate_data['TABLE_FIELDS_NAME'] = table_field_name
        self.replate_data['TABLE_FIELDS_VALUE'] = table_field_value
            
    def isFNumber(self, type):
        if self.number_data_type.count(type)>=1:
            return True
        else:
            return False
    
    def isFString(self, type):
        if self.string_data_type.count(type)>=1:
            return True
        else:
            return False
        
    def getDateType(self, type):
        if self.isFString(type):
            return 'String'
        elif self.isFNumber(type):
            return 'Number'
    
    def autoTreeField(self, field, field_name):
        form_html = '<?php $field["field_name"]="%s[%s]"; $field["id"]="%s"; $field["name"]="%s"; $field["parent"]="%s"?>\n' % (self.var, field_name,  field[field_name][3], field[field_name][2], field[field_name][4])
        form_html += '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td ><?php echo listCategories((isset($row->%s)?$row->%s:""), %s, "%s");?>\n</td>\n</tr>\n' % (field_name.capitalize(), field_name,field_name, field_name, '$field', field[field_name][1])
        return form_html

    def autoFileField(self, field, type):
        select_image = "<input type='file' name='%s[%s]' />" % (self.var, field)
        form_html = '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >%s\n</td>\n</tr>\n' % (field, field.capitalize(),select_image)
        delete_file = '<input type="checkbox" name="%s[delete_files][%s]"/> <a href="<?=JURI::root().\'administrator/components/%s/assets/upload/\'.$row->%s?>">Download</a>' % (self.var, field, self.component_name, field)
        form_html += '<?php if($row->%s!=\'\'){?><tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >%s\n</td>\n</tr>\n<?php } ?>' % (field, "delete_"+field, "Delete "+field.capitalize(), delete_file)
        return form_html

    def autoListField(self, field, type):
        select_image = "<?php echo JHTML::_('list.images','%s[%s]',(isset($row->%s)?$row->%s:''),'onchange=\"window.document.imagelib.src=\\'\'.JURI::root().$image_path_from_select.\'\\'+this.value\"',$image_path_from_select);?><br/><img name='imagelib' src='<?php echo JURI::root().$image_path_from_select.$row->%s?>' />"
        select_image = (select_image) % ( self.var, field, field , field, field)
        form_html = '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >%s\n</td>\n</tr>\n' % (field, field.capitalize(),select_image)
        return form_html

    def autoDateField(self, field, type):
        calendar_img = '<img class="calendar" src="templates/system/images/calendar.png" alt="calendar" onclick="return showCalendar(\'%s\', \'%s\');" />' % (field, self.php_date_time)
        form_html = '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >\n<input class="inputbox" type="text" name="%s[%s]" id="%s" size="60" maxlength="255" value="<?php echo (isset($row->%s)?$row->%s:""); ?>" /> %s\n</td>\n</tr>\n' % (field, field.capitalize(),self.var,field,field,field,field, calendar_img)
        return form_html

    def autoBooleanField(self, field, type):
        select_option = "<select name='%s[%s]' id='%s'><option <?php if(isset($row->%s)){ echo ($row->%s==1)?'selected=\"selected\"':'';}?> value='1'>Yes</option><option <?php if(isset($row->%s)){ echo ($row->%s==0)?'selected=\"selected\"':'';}?> value='0'>No</option></select>" % (self.var, field, field, field, field, field)
        form_html = '<tr>\n<td class="key">\n<label for="%s">\n<?php echo JText::_("%s");?>:</label>\n</td>\n<td >%s\n</td>\n</tr>\n' % (field, field.capitalize(), select_option)
        return form_html