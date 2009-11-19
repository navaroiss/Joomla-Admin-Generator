Joomla Admin Generator (jag) - The first version of jag.

There are three questions, if you are a joomla developer
--------------------------------------------------------
- How to automatically build a joomla component? Do you know some tools help me do that?
- Do you like hand coding for CRUD actions, for every component?
- And how to build a installation package?


I have one anwser
-----------------
- Jag can do that. Let belive me and run it right now :-) 
- [Get one jag](http://github.com/navaroiss/Joomla-Admin-Generator/archives/master)

How to run?
-----------
linux/unix:
	python jag.py -c config.xml
windows:
	c:\\python26\python.exe jag.py -c config.xml

An example
-----------
The content in config.xml

	<component name="com_test" author="Your name" email="your.email@gmail.com">
		<table name="test_category" sort_name="category">
			<field type="int" length="11" auto_increment="true" primary_key="true">id</field>
			<field type="varchar" length="255">name</field>
			<field type="text">value</field>
			<field type="int" length="10" belong="id">parent</field>
		</table>
		<table name="test_entry" sort_name="entry">
			<field type="int" length="11" auto_increment="true" primary_key="true">id</field>
			<field type="varchar" length="250">title</field>
			<field type="date" design="%Y-%m-%d">date</field>
			<field type="text">content</field>
		        <field type="listfile" folder="smilies">icon</field>
			<field type="file" file_type="image">image</field>
			<field type="file" file_type="document, compress">document</field>
			<field type="tree" table_name="test_category" table_field_name="name" table_field_primary="id" table_field_parent="parent">catid</field>
		        <field type="boolean">published</field>
		</table>
	</component>

Video
------
Download:

- [link 1](http://github.com/navaroiss/Joomla-Admin-Generator/downloads)
- [link 2 - best quality](http://joomla-admin-generator.googlecode.com/files/how-it-work.ogv)

The field type to be supported
-------------------------------

Normal:

- int
- varchar
- text
- date
- boolean


Special:

- file *to upload images, document...*
- listfile *to list all file in a directory*
- tree *to show a multi-level category*
