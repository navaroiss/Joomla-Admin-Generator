<?php
	/*
	** Generated by Joomla Admin Generator
	** Author: {AUTHOR_NAME}
	** Email: {AUTHOR_EMAIL}
	** 
	** Component:  {COMPONENT_PATH}
	** Helper
	** File: {FILE_NAME}
	** Time: {TIME}
	*/

 /*
 ** $field[field_name], $field[name], $field[parent], $field[id]
 ** 
 */
 
 function listCategories($parent=0, $field = array(), $table, $js = '', $root_value=0)
 {
  $conf =& JFactory::getConfig();
  $field_name = $field['field_name'];
  $html = "<select $js name='".$field_name."'>";
  $s = ($parent==0)?'selected="selected"':'';
  $html .= "<option value='$root_value' $s>ROOT</option>"; 
  $selcat="SELECT * from ".$conf->getValue('config.dbprefix')."$table order by name ASC";
  $selcat2= mysql_query($selcat) or die("Could not select category");
  $html .= traverse(0,0,$selcat2, $field, $parent);
  $html .= "</select><br>";
  return $html;
 }

 function traverse($root, $depth, $sql, $field, $parent=0) 
 { 
     $row=0;
     $id = $field['id'];
     $name = $field['name'];
     $field_parent = $field['parent'];
     $t = '';

     while ($acat = mysql_fetch_array($sql)) 
     { 
          if ($acat[$field_parent] == $root) 
          { 
		$s = ($parent==$acat[$id])?'selected="selected"':'';
               $t .= "<option value='" . $acat[$id] . "' $s>"; 
               $j=0; 
               while ($j<$depth) 
               {     
                     $t .= "-";
                    $j++; 
               } 
               if($depth>0)
               {
                 $t .= "-";
               }
               $t .= $acat[$name] . "</option>"; 
               @mysql_data_seek($sql,0); 
               $t .= traverse($acat[$id], $depth+1,$sql, $field, $parent); 
          } 
          $row++; 
          @mysql_data_seek($sql,$row); 
     } 
     return $t;
 }	
 ?>
