#!/usr/bin/env python

#
# Linux Desktop Testing Project http://www.gnomebangalore.org/ldtp
#
# Author:
#    Khasim Shaheed <khasim.shaheed@gmail.com>
#
# Copyright 2004 Novell, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#

import gtk
import gtk.glade
import webbrowser
import sys 
import os.path

import dialogs, xmldatadialog, syntax

if sys.version_info[1] < 4:
	print 'You should have Python version 2.4 or greater installed to run this program'
	sys.exit(0)

class LDTPUIManager:
    ui = '''<ui>
     <menubar name="Menubar">
       <menu action="File">
         <menuitem action="New"/>
         <menuitem action="Open"/>
         <menuitem action="Save"/>
         <menuitem action="Save As"/>
	 <separator/>
         <menuitem action="Close"/>
         <menuitem action="Quit"/>
       </menu>
       <menu action="Edit">
         <menuitem action="Cut"/>
         <menuitem action="Copy"/>
         <menuitem action="Paste"/>
       </menu>
       <menu action="View">
	 <menuitem action="Script Selection"/>
       </menu>		
       <menu action="Format">
         <menuitem action="Indent Region"/>
         <menuitem action="Dedent Region"/>
       </menu>
       <menu action="Tools">
         <menuitem action="Record"/>
	 <menuitem action="Data XML"/>
       </menu>
       <menu action="Help">
         <menuitem action="Contents"/>
         <menuitem action="About"/>
       </menu>
     </menubar>
     <toolbar name="Toolbar">
       <toolitem action="New"/>
       <toolitem action="Open"/>
       <toolitem action="Save"/>
       <separator/>
       <toolitem action="Cut"/>
       <toolitem action="Copy"/>
       <toolitem action="Paste"/>		
       <separator/>
       <toolitem action="Record"/>
     </toolbar>
    </ui>'''

    sl_ui = '''<ui>
     <menubar name="Menubar">
       <menu action="Options">
         <menuitem action="Add Group"/>
         <menuitem action="Remove Group"/>
         <menuitem action="Add Script(s)"/>
         <menuitem action="Remove Script"/>
	 <menuitem action="Add Datafile"/>
       </menu>
     </menubar>	
     <toolbar name="Toolbar">
     </toolbar>
    </ui> '''	

    def __init__(self):
	# Create Dictionaries for untitled numbers and opened files uris
	self.untitled_numbers = {}
	self.doc_names = {}
	self.num_pages = 0
	
	# Data related to Script Selection Window
	self.script_selection_exists = False

        # Create the toplevel window
        self.window = gtk.Window()
	self.window.set_title('LDTP Editor')
        self.window.set_default_size(650, 500)
        vbox = gtk.VBox()
        self.window.add(vbox)

        # Create a LDTPUIManager instance
        self.uimanager = gtk.UIManager()

        # Add the accelerator group to the toplevel self.window
        accelgroup = self.uimanager.get_accel_group()
        self.window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('LDTPUIManager')
        self.actiongroup = actiongroup

	# Create a ToggleAction
	actiongroup.add_toggle_actions([('Script Selection', None, 'Scri_pt Selection', '<Control>p',
				        'Show Script Selection Window', self.script_selection_cb)])
	
        # Create actions
        actiongroup.add_actions([('New', gtk.STOCK_NEW, '_New', None,
				  'Create a new script', self.new_cb),
				 ('Open', gtk.STOCK_OPEN, '_Open', None,
				  'Open a file', self.open_cb),
				 ('Save', gtk.STOCK_SAVE, '_Save', None,
				  'Save the current file', self.save_cb),
				 ('Save As', gtk.STOCK_SAVE_AS, 'Save _As', '<Shift><Control>s',
				  None, self.saveas_cb),
				 ('Close', gtk.STOCK_CLOSE, '_Close', None,
				  None, self.close_cb),
				 ('Quit', gtk.STOCK_QUIT, '_Quit', None,
                                  'Quit the Program', self.quit_cb),
				 ('Cut', gtk.STOCK_CUT, 'Cu_t', None,
				  'Cut the selection', self.on_cut_activate_cb),
				 ('Copy', gtk.STOCK_COPY, '_Copy', None,
				  'Copy the selection', self.on_copy_activate_cb),
				 ('Paste', gtk.STOCK_PASTE, '_Paste', None,
				  'Paste the Clipboard', self.on_paste_activate_cb),
				 ('Indent Region', None, '_Intedent Region', '<Control>i',
				  None, self.indent_region_cb),
				 ('Dedent Region', None, '_Dedent Region', '<Control>d',
				  None, self.dedent_region_cb),
				 ('Record', gtk.STOCK_HARDDISK, '_Record', '<Control>r',
				  'Start recording', None),
				 ('Data XML', None, 'Data XML', None,
				  'Create Data XML file', self.create_xml_data_file_cb),
				 ('Contents', gtk.STOCK_HELP, '_Contents', 'F1',
				  None, None),
				 ('About', gtk.STOCK_ABOUT, '_About', None,
				  None, self.about_cb),
                                 ('File', None, '_File'),
				 ('Edit', None, '_Edit'),
				 ('View', None, '_View'),
				 ('Format', None, 'Fo_rmat'),
				 ('Tools', None, '_Tools'),
				 ('Help', None, '_Help')])
                                 
        # Add the actiongroup to the self.uimanager
        self.uimanager.insert_action_group(actiongroup, 0)

        # Add a UI description
        self.uimanager.add_ui_from_string(self.ui)

        # Create a MenuBar
        menubar = self.uimanager.get_widget('/Menubar')
        vbox.pack_start(menubar, False)

        # Create a Toolbar
        toolbar = self.uimanager.get_widget('/Toolbar')
        vbox.pack_start(toolbar, False)
	
	# Create an Horizontal Pane
	self.hpane = gtk.HPaned()
	vbox.pack_start(self.hpane, True)

	# Create a Notebook
	self.notebook = gtk.Notebook()
	self.notebook.set_scrollable (True)
	self.notebook.connect ('switch-page', self.switch_page_cb)
	self.new_cb (None)
	self.hpane.add2(self.notebook)

	# FIXME Have to make use of this status bar to show line, col numbers etc..
	# Create Statusbar
	self.statusbar = gtk.Statusbar()
	vbox.pack_end(self.statusbar, False)
	self.context_id = self.statusbar.get_context_id('My Editor')

	# Create Clipboard
	self.clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), 'CLIPBOARD')

        self.window.connect('delete_event', self.quit_cb)
        self.window.show_all()
        return
   
    def script_selection_cb (self, action):
	if action.get_active():
		if not(self.script_selection_exists):
			self.script_selection_exists = True

			self.script_selection_frame = gtk.Frame()
			self.script_selection_frame.set_size_request (200, 400)
			self.hpane.add1(self.script_selection_frame)
	
			vbox = gtk.VBox()
			scrolled_window = gtk.ScrolledWindow()
        		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			self.script_selection_frame.add(vbox)
			
			hbox = gtk.HBox()
			sl_uimanager = gtk.UIManager()
			sl_actiongroup = gtk.ActionGroup('LDTPUIManager')
			sl_actiongroup.add_actions([('Add Group', None, 'Add Group', None,
						     'Add a Group', self.add_group_cb),	
						    ('Remove Group', None, 'Remove Group', None,
						     'Remove a Group', self.remove_group_cb),	
						    ('Add Script(s)', None, 'Add Script(s)', None,
						     'Add one or more Script(s)', self.add_script_cb),	
						    ('Remove Script', None, 'Remove Script', None,
						     'Remove a Script', self.remove_script_cb),	
						    ('Add Datafile', None, 'Add Datafile', None,
						     'Add a Datafile', self.add_data_cb),	
						    ('Options', None, 'Options')])

			sl_uimanager.insert_action_group(sl_actiongroup, 0)
			sl_uimanager.add_ui_from_string(self.sl_ui)
			
			sl_menubar = sl_uimanager.get_widget('/Menubar')
			hbox.pack_start(sl_menubar, False)

			sl_toolbar = sl_uimanager.get_widget('/Toolbar')
			image = gtk.image_new_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_MENU)
			button = gtk.Button()
			button.add(image)
			button.set_relief(gtk.RELIEF_NONE)
			button.connect('clicked', self.generate_xml_cb)
			sl_toolbar.add(button)

			image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
			button = gtk.Button()
			button.add(image)
			button.set_relief(gtk.RELIEF_NONE)
			button.connect('clicked', self.close_script_selection_cb)
			sl_toolbar.add(button)
			hbox.pack_end(sl_toolbar, False)

			vbox.pack_start(hbox, False)
			vbox.pack_start(scrolled_window, True)
			
			self.treestore = gtk.TreeStore(str, str)
			self.treeview = gtk.TreeView(self.treestore)
        		cell_script = gtk.CellRendererText()
			cell_data = gtk.CellRendererText()

			self.treeview.insert_column_with_attributes (-1, 'Script Files', cell_script, text=0)
			self.treeview.insert_column_with_attributes (-1, 'Data Files', cell_data, text=1)

			scrolled_window.add (self.treeview)
			self.window.show_all()
		else:
			self.script_selection_frame.show()
	else:
		if self.script_selection_exists:
			self.script_selection_frame.hide()

    def close_script_selection_cb (self, b):
	self.script_selection_frame.destroy()
	script_selection_menu_item = self.uimanager.get_widget('/Menubar/View/Script Selection')
	script_selection_menu_item.set_active(False)
	self.script_selection_exists = False

    def add_group_cb (self, b):
	iter = self.treestore.insert_before(None, None)
	self.treestore.set_value(iter, 0, 'Group')

    def add_script_cb (self, b):
	iter = self.get_iter_at_selected_row()

	if not (iter):
		xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING, 
					      'Select a group and then try adding a script.')	
	else:
		if self.iter_isa_group (iter):
			open_dialog = dialogs.file_dialog ('Open...', self.window,
							   gtk.FILE_CHOOSER_ACTION_OPEN, multiple_selection=True)
	
			response = open_dialog.run()
			
			if response == gtk.RESPONSE_OK:
				scripts = open_dialog.get_filenames()
				open_dialog.destroy()
	
				for i in range (0, len(scripts)):
					file = os.path.split (scripts[i])[1]
					self.treestore.append(iter, [file, None])
			else:
				open_dialog.destroy()
	
			self.treeview.expand_all()
		else:
			xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING,
						  'Script can be added only if a group is selected.')	
    def iter_isa_group (self, iter):
    	if iter:
	    	temp = self.treestore.get_iter_first()
		model = self.treeview.get_model()
		
		while temp:
			if model.get_value (temp, 0) == model.get_value (iter, 0): return True
			temp = self.treestore.iter_next (temp)

	return False

    def add_data_cb (self, b):
	iter = self.get_iter_at_selected_row()
	
	if not (iter):
		xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING, 
					      'Select a script and then try adding data file.')
	else:		
		if self.iter_isa_script (iter):
			open_dialog = dialogs.file_dialog ('Open...', self.window,
							   gtk.FILE_CHOOSER_ACTION_OPEN)
	
			response = open_dialog.run()
			
			if response == gtk.RESPONSE_OK:
				data = open_dialog.get_filename()
				open_dialog.destroy()
				data_file = os.path.split (data)[1]
				self.treestore.set_value(iter, 1, data_file)
			else:
				open_dialog.destroy()
		else:
			xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING,
						      'Data file can be added only if a script is selected.')

    def iter_isa_script (self, iter):
    	parent = self.treestore.get_iter_first()
	model = self.treeview.get_model()

	while parent:
		child = self.treestore.iter_children (parent)
		
		while child:
			if model.get_value (child, 0) == model.get_value (iter, 0): return True
			child = self.treestore.iter_next (child)
			
		parent = self.treestore.iter_next (parent)	
	
	return False
	
    def remove_group_cb (self, b):
	iter = self.get_iter_at_selected_row()

	if not (iter):
		xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING, 
					      'Select a group and then try remove group.')
	else:	
		if self.iter_isa_group (iter):
			self.treestore.remove(iter)
		else:
			xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING, 
					      'The selected item is not a group.')

    def remove_script_cb (self, b):
	iter = self.get_iter_at_selected_row()

	if not (iter):
		xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING, 
					      'Select a script and then try remove script.')
	else:	
		if self.iter_isa_script (iter):
			self.treestore.remove(iter)
		else:
			xmldatadialog.message_dialog (self.window, gtk.MESSAGE_WARNING, 
					      'The selected item is not a script.')

    def get_iter_at_selected_row (self):
	treeselection = self.treeview.get_selection()
	model, iter = treeselection.get_selected()
	return iter

    def generate_xml_cb (self, b):
	parent = self.treestore.get_iter_first()
    	log_file_name = None
	appmap_name = None
	overwrite_log_file = True
	
	if parent:
		gladefile_path = '.'
		if '/usr/lib/ldtpeditor' in sys.path:
			gladefile_path = '/usr/lib/ldtpeditor'
			
		gladefile = gladefile_path + "/log_file.glade"
		glade_xml_object = gtk.glade.XML (gladefile, "dialog")
		
		dialog = glade_xml_object.get_widget ("dialog")
		log_file_entry = glade_xml_object.get_widget ("log_file_entry")
		appmap_entry = glade_xml_object.get_widget ("appmap_entry")
		browse_log_file = glade_xml_object.get_widget ("browse_log_file")
		browse_appmap = glade_xml_object.get_widget ("browse_appmap")
		check_overwrite = glade_xml_object.get_widget ("overwrite")

		browse_log_file.connect ('clicked', self.browse_file, log_file_entry, 'log')
		browse_appmap.connect ('clicked', self.browse_file, appmap_entry, 'appmap')

		while True:
			response = dialog.run ()
			if response == gtk.RESPONSE_OK:
				log_file_name = os.path.split (log_file_entry.get_text ())[1]
				appmap_name = os.path.split (appmap_entry.get_text ())[1]
				overwrite_log_file = check_overwrite.get_active ()
				if not(log_file_name):
					xmldatadialog.message_dialog (dialog, gtk.MESSAGE_WARNING,
								         'Enter a valid log file name')	
				else: break
	
			else: break		
		
		dialog.destroy ()

	if log_file_name:
	    	file = None
    		save_dialog = dialogs.file_dialog ('Save XML file As...', self.window,
						   gtk.FILE_CHOOSER_ACTION_SAVE, 
						   default_file='Untitled.xml')

		file, replace = self.get_file_to_save (save_dialog)
		
		if file:
			fp = open (file, 'w')
			
			parent = self.treestore.get_iter_first()
			model = self.treeview.get_model()
			xml = '<?xml version="1.0"?>\n<ldtp>\n'
			
			if overwrite_log_file:
				xml = xml + ' <logfileoverwrite>1</logfileoverwrite>\n'
			if not(overwrite_log_file):
				xml = xml + ' <logfileoverwrite>0</logfileoverwrite>\n'

			xml = xml + ' <logfile>' + log_file_name + '</logfile>\n'
			if appmap_name:
				xml = xml + ' <appmapfile>' + appmap_name + '</appmapfile>\n'

			while parent:
				xml = xml + ' <group>\n' 
				child = self.treestore.iter_children(parent)
		
				while child:
					xml = xml + '  <script>\n'
					xml = xml + '   <name>'+model.get_value (child, 0)+'</name>\n'
	
					data_file = model.get_value (child, 1)
					if data_file:
						xml = xml + '   <data>' + data_file + '</data>\n'
	
					xml = xml + '  </script>\n'
					child_next = self.treestore.iter_next(child)
					child = child_next
		
				xml = xml + ' </group>\n'	
				parent_next = self.treestore.iter_next(parent)
				parent = parent_next
			
			xml = xml + '</ldtp>\n'
	
			fp.write (xml)
			fp.close ()

    def browse_file (self, button, entry, type):
	if type == 'appmap':
	    	dialog = dialogs.file_dialog ('Select appmap file...', None, 
						   gtk.FILE_CHOOSER_ACTION_OPEN)
	elif type == 'log':
		dialog = dialogs.file_dialog ('Save log file as...', None, 
						   gtk.FILE_CHOOSER_ACTION_SAVE,
						   default_file='Untitled.xml')
	
	response = dialog.run ()
	
	if response == gtk.RESPONSE_OK:
		file = dialog.get_filename ()
		dialog.destroy ()
		entry.set_text (file)
	else:
		dialog.destroy ()
	
    def create_xml_data_file_cb (self, b):
	save_dialog = dialogs.file_dialog ('Save XML Data file As...', self.window, 
					   gtk.FILE_CHOOSER_ACTION_SAVE, 
					   default_file='Untitled.xml')

	file, replace = self.get_file_to_save (save_dialog) 
	
	if file:	
		xmldatadialog.data_xml_cb (file, replace)

    def switch_page_cb (self, notebook, page, page_num):
	if self.num_pages > 0:
		if self.doc_names.has_key(page_num):
			page_title = self.doc_names[page_num]
			self.window.set_title (page_title)	
	
    def quit_cb (self, b, junk=None):
	# Check if all the opened documents are saved or not before quitting
	num_opened_docs = self.notebook.get_n_pages()
	num_unsaved_docs = 0

	if num_opened_docs > 0:
		for i in range (0, num_opened_docs):
			widget = self.notebook.get_nth_page(i)
			sourceview = (widget.get_child()).get_child()
			txtbuf = sourceview.get_buffer()

			if txtbuf.get_modified():
				num_unsaved_docs = num_unsaved_docs + 1

	if num_unsaved_docs > 0:
		prim_text = 'There is(are) ' + str(num_unsaved_docs) + ' document(s) with unsaved changes. Save changes before closing'
		sec_text = 'If you don\'t save, all your changes will be permanently lost.'
		buttons = ('Close without saving', gtk.RESPONSE_REJECT,
			   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)

		message_dialog = dialogs.message_dialog (self.window, gtk.MESSAGE_WARNING, buttons, 
							gtk.RESPONSE_CANCEL, prim_text, sec_text) 
		response = message_dialog.run()
		
		if response == gtk.RESPONSE_CANCEL:
			message_dialog.destroy()
			return True
		else:
			None

	del self.doc_names
	del self.untitled_numbers
	self.window.destroy()
       	gtk.main_quit()

    def new_cb(self, b):
	untitled_number = self.get_untitled_number()
	scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

	if sys.version_info[2] > 0: 
		import gtksourceview
		
       		sourceview = gtksourceview.SourceView()
		sourceview.set_show_line_numbers (True)
		sourceview.set_auto_indent (True)
		# sourceview.set_highlight_current_line (True)
	else:
		sourceview = gtk.TextView ()
		
        txtbuf = sourceview.get_buffer()
	txtbuf.connect ('changed', self.on_modified)
	
	txtbuf.create_tag ("python_keyword", foreground="#a52a2a")
    	txtbuf.create_tag ("python_string",  foreground="#ff00ff")
    	txtbuf.create_tag ("python_comment", foreground="#0000ff")
    	txtbuf.create_tag ("python_builtin", foreground="#2e8b57")
    	txtbuf.create_tag ("python_function", foreground="#1db8ca")

       	scrolled_window.add(sourceview)
        sourceview.set_editable(True)

	# Append the scrolled window as a notebook page
	frame = gtk.Frame()
	frame.add(scrolled_window)
	
	# Construct label for a notebook page
	hbox = gtk.HBox()
	default_label = 'Untitled ' + str(untitled_number) 
	label = gtk.Label(default_label)
	hbox.pack_start(label, False)
	image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
	button = gtk.Button()
	button.add(image)
	button.set_relief(gtk.RELIEF_NONE)
	button.set_size_request (18, 18)
	button.connect('clicked', self.close_cb) 
	hbox.pack_end(button, False)

	self.notebook.append_page(frame, hbox) 
	self.add_file_name(self.num_pages, default_label)
	self.window.set_title (default_label + '-LDTP Editor')
	self.num_pages = self.num_pages + 1

	hbox.show_all()
	self.window.show_all()
	self.notebook.set_current_page (self.num_pages-1)
	sourceview.grab_focus()	

    def open_cb(self, b):
	# Open File chooser dialog
	open_dialog = dialogs.file_dialog ('Open...', self.window, gtk.FILE_CHOOSER_ACTION_OPEN)
	response = open_dialog.run()

	if response == gtk.RESPONSE_OK:
		file = open_dialog.get_filename()
		infile = open (file, 'r')

		if infile:
			file_content = infile.read()
		infile.close()
		
		self.new_cb(None)

		sourceview = self.get_sourceview()
		txtbuf = sourceview.get_buffer()
		page = self.notebook.get_current_page()
		widget = self.notebook.get_nth_page(page)
		hbox = self.notebook.get_tab_label(widget)
		hbox_children = hbox.get_children()

		# Get the file name and set it as the label of page
		file_name = os.path.split (file)[1]
		self.add_file_name(page, file)
		self.window.set_title(file + ' - LDTP Editor')

		prev_label = self.get_label()

		self.check_and_release_number(prev_label)
		
		hbox_children[0].set_label(file_name)
		self.notebook.set_tab_label(widget, hbox)
		txtbuf.set_text(file_content)
		txtbuf.set_modified(False)
		txtbuf.place_cursor (txtbuf.get_start_iter())
		open_dialog.destroy()
	else:
		open_dialog.destroy()

    def saveas_cb(self, b):
	sourceview = self.get_sourceview()

	if sourceview:
		txtbuf = sourceview.get_buffer()
		prev_label = self.get_label()
		
		save_dialog = dialogs.file_dialog ('Save As...', self.window,
						   gtk.FILE_CHOOSER_ACTION_SAVE, default_file=prev_label)
		
		file, replace = self.get_file_to_save (save_dialog)	

		if file:
			fp = open (file, 'w')
	        	text = txtbuf.get_text (txtbuf.get_start_iter (), txtbuf.get_end_iter (), include_hidden_chars = True)
	        	fp.write (text)
	        	txtbuf.set_modified (False)
	        	fp.close ()
	
			page = self.notebook.get_current_page()
			widget = self.notebook.get_nth_page(page)
			hbox = self.notebook.get_tab_label(widget)
			hbox_children = hbox.get_children()
	
			self.check_and_release_number(prev_label)
		
			# Get the file name and set it as the label of page
			file_name = os.path.split (file)[1]
			self.add_file_name(page, file)
			self.window.set_title (file + ' - LDTP Editor')
			hbox_children[0].set_label(file_name)
			self.notebook.set_tab_label(widget, hbox)
		

    def save_cb(self, b):
	file_saved_flag = False
	file_name = self.get_label()

	# Check whether the document is saved atleast once
	# If yes don't open the save as dialog
	i = 0
	while True:
		if self.doc_names.has_key(i):
			temp_file = self.doc_names[i]
		else:
			break

		if temp_file.find ('/') >= 0:
			if (os.path.split (temp_file)[1] == file_name):
				file_saved_flag = True
				break
		
		i = i+1
	
	if file_saved_flag:
		sourceview = self.get_sourceview()
		txtbuf = sourceview.get_buffer()

		if txtbuf.get_modified():
			fp = open (file_name, 'w')
	       		text = txtbuf.get_text (txtbuf.get_start_iter (), txtbuf.get_end_iter (), include_hidden_chars = True)
		       	fp.write (text)
       			txtbuf.set_modified (False)
		       	fp.close ()
	else:
		self.saveas_cb(None)
	
    def close_cb(self, b):
	# If the document is not saved throw a warning message
	response = None
	page = None
	sourceview = None
	label = None

	if b.get_name() == 'Close': 
		if self.notebook.get_n_pages():
			page = self.notebook.get_current_page ()

			widget = self.notebook.get_nth_page (page)
			hbox = self.notebook.get_tab_label (widget)
			label = hbox.get_children()[0].get_label()

			sourceview = (widget.get_child()).get_child()
		
	else:
		hbox = b.get_parent()
		label = hbox.get_children()[0].get_label()

		# FIXME while closing files with same names but in different directories may not close  
		# the requested one. So this logic has to be refined.
		for i in range(0, len(self.doc_names)):
			doc_name = self.doc_names[i]
			if os.path.split (doc_name)[1] == label:
				page = i	
				break

		widget = self.notebook.get_nth_page(page)
		sourceview = (widget.get_child()).get_child()

	if sourceview:
		txtbuf = sourceview.get_buffer()

		if txtbuf.get_modified():
			prim_text = 'Save the changes to document \"' + label +'\" before closing?'	
			sec_text = 'If you don\'t save, all the changes you have made will be permanently lost.'
			buttons = ('Close without saving', gtk.RESPONSE_REJECT,
				   gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				   gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT)
			
			message_dialog = dialogs.message_dialog (self.window, gtk.MESSAGE_WARNING, buttons, 
			                 gtk.RESPONSE_ACCEPT, prim_text, sec_text)
			response = message_dialog.run()
			
			if response == gtk.RESPONSE_REJECT:
				message_dialog.destroy()

			elif response == gtk.RESPONSE_ACCEPT:
				message_dialog.destroy()
				self.save_cb(None)
				return
			else:
				message_dialog.destroy()
				return

	if label:
		self.check_and_release_number(label)

		if not(page == None):
			self.remove_file_name(page)
			self.notebook.remove_page(page)

	if self.num_pages == 0:
		self.window.set_title ('LDTP Editor')

    def about_cb(self, b):
	# Create about dialog
	image_path = '.'
	about_dialog = gtk.AboutDialog()

	about_dialog.set_name('LDTP Editor')
	about_dialog.set_version('0.1.0')
	about_dialog.set_comments('LDTP Editor is a lightweight text editor for\nLinux Desktop Testing Project')
	about_dialog.set_copyright('Copyright \xc2\xa9 2005 Khasim Shaheed')

	gtk.about_dialog_set_url_hook(self.open_url, None)
	about_dialog.set_website_label('http://www.gnomebangalore.org/ldtp')

	about_dialog.set_authors(['Khasim Shaheed <sshaik@novell.com>'])
	
	if '/usr/lib/ldtpeditor' in sys.path:
		image_path = '/usr/lib/ldtpeditor'
		
	logo = gtk.gdk.pixbuf_new_from_file(image_path + '/ldtp-logo-small.png')
	about_dialog.set_logo (logo)

	about_dialog.show()
	
    def open_url(self, a=None, b=None, c=None):
	webbrowser.open('http://www.gnomebangalore.org/ldtp')

    def on_cut_activate_cb(self, b):
	sourceview = self.get_sourceview()

	if sourceview:
		txtbuf = sourceview.get_buffer()
		txtbuf.cut_clipboard(self.clipboard, sourceview.get_editable())
	

    def on_copy_activate_cb(self, b):
	sourceview = self.get_sourceview()

	if sourceview:
		txtbuf = sourceview.get_buffer()
		txtbuf.copy_clipboard(self.clipboard)

    def on_paste_activate_cb(self, b):
	sourceview = self.get_sourceview()

	if sourceview:
		txtbuf = sourceview.get_buffer()
		txtbuf.paste_clipboard(self.clipboard, None, sourceview.get_editable())

    def get_file_to_save (self, save_dialog):
    	file = None
	replace = False
    	while True:
		response = save_dialog.run()
			
		if response == gtk.RESPONSE_OK:
			file = save_dialog.get_filename()
				
			if os.path.exists(file):
				prim_text = 'A file named \"' + file + '\" already exists.'	
				sec_text = 'Do you want to replace it with the one you are saving?'
				buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				           'Replace', gtk.RESPONSE_ACCEPT)

				message_dialog = dialogs.message_dialog (save_dialog, gtk.MESSAGE_QUESTION,
							buttons, gtk.RESPONSE_CANCEL, prim_text, sec_text)
				response = message_dialog.run()
				
				if response == gtk.RESPONSE_ACCEPT:
					message_dialog.destroy()
					replace = True
				else:	
					message_dialog.destroy()
					file = None
					continue
	
			save_dialog.destroy()
		else:
			save_dialog.destroy()
		
		break
	
	return (file, replace)
		
    def on_modified (self, buffer):
    	obj = syntax.PythonSyntax()
    	self.highlight (obj, buffer)

    def highlight (self, syntax_object, buffer):
	start, end = buffer.get_bounds ()
	buffer.remove_all_tags (start, end)
		
	code = buffer.get_text (start, end)

	for tag, (srow, scol), (erow, ecol) in syntax_object.scan (code):
		start = buffer.get_iter_at_line_offset (srow-1, scol)
		end   = buffer.get_iter_at_line_offset (erow-1, ecol)
		buffer.apply_tag_by_name (tag, start, end)

    def get_sourceview(self):
	# Get the sourceview widget of current active page
	if self.notebook.get_n_pages():
		page = self.notebook.get_current_page()
		widget = self.notebook.get_nth_page(page)
		sourceview = (widget.get_child()).get_child()
		return sourceview

    def get_label(self):
	# Get the label of current active page tab
	if self.notebook.get_n_pages() > 0:
		page = self.notebook.get_current_page()
		widget = self.notebook.get_nth_page(page)
		hbox = self.notebook.get_tab_label(widget)
		hbox_children = hbox.get_children()
		prev_label = hbox_children[0].get_label()
		return prev_label

    def get_untitled_number(self):
	# Allocate an untitled number for new page
	i = 1

	while True:
		if not(self.untitled_numbers.has_key(i)):
			self.untitled_numbers[i] = i
			return i
		i = i + 1

    def release_untitled_number(self, n):
	# Release the given untitled number from the dictionary
	if self.untitled_numbers.has_key(n):
		del self.untitled_numbers[n]

    def add_file_name(self, page, file_name):
	# Store the file_name in a dictionary
	self.doc_names[page] = file_name

    def remove_file_name(self, page):
	# Remove the file_name from the dictionary
	if self.doc_names.has_key(page):
		del self.doc_names[page]
		self.num_pages = self.num_pages-1

		# Reorder pages
		temp = {}
		keys = self.doc_names.keys()
	
		for i in range (0, len(self.doc_names)):
			j = keys[i]
			temp[i] = self.doc_names[j]
		
		self.doc_names.clear()
		self.doc_names = temp

    def check_and_release_number(self, prev_label):
	# Check if prev_label contains untitled number and release it
	release_number = ''

	if prev_label.find('Untitled') >= 0:
		release_number = prev_label[9:]

	if release_number is not '':
		for i in range(1, 10):
			if release_number[:1] == str(i):
				self.release_untitled_number(int(release_number))
				break

    def indent_region_cb(self, b):
        text = '\t'
	sourceview = self.get_sourceview()

	if sourceview:
		txtbuf = sourceview.get_buffer()
	        first, last = txtbuf.get_selection_bounds ()
		start_line = first.get_line()
		end_line = last.get_line()
		line = start_line
		num_lines = end_line-start_line + 1

	        for i in range (num_lines):
	                iter = txtbuf.get_iter_at_line (line)
			line = line + 1

			# don't add indentation on empty lines
			if iter.ends_line():
				continue

			txtbuf.insert(iter, text)

    def dedent_region_cb(self, b):
	sourceview = self.get_sourceview()

	if sourceview:
		txtbuf = sourceview.get_buffer()
	        first, last = txtbuf.get_selection_bounds ()
		start_line = first.get_line()
		end_line = last.get_line()
		line = start_line
		num_lines = end_line-start_line + 1

	        for i in range (num_lines):
	                iter = txtbuf.get_iter_at_line(line)
			iter1 = txtbuf.get_iter_at_line(line)
			
			# If the indentation is filled with tabs
			if iter.get_char() == '\t':
				iter1.forward_char()
				txtbuf.delete(iter, iter1)	

			# If the indentation is filled with spaces
			elif iter.get_char() == ' ':
				spaces = 0
				
				while (iter1.ends_line() == False):
					if iter1.get_char() == ' ':
						spaces = spaces+1
					else:
						break
					iter1.forward_char()
				
				if spaces > 0:
					tabs = 0
					tabs = spaces/6
					spaces = spaces - (tabs * 6)

					if spaces == 0:
						spaces = 6

					iter1 = txtbuf.get_iter_at_line(line)
					iter1.forward_chars(spaces)
					txtbuf.delete(iter, iter1) 
			line = line + 1

if __name__ == '__main__':
    LDTPUIManager()
    gtk.main()
