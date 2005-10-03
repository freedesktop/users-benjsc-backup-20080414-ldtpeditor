import gtk
import gtk.glade
import sys

def data_xml_cb (output_file, replace):
	gladefile_path = '.'
	if '/usr/lib/ldtpeditor' in sys.path:
		gladefile_path = '/usr/lib/ldtpeditor'

	gladefile = gladefile_path + "/data_xml.glade"
	glade_xml_object = gtk.glade.XML (gladefile, "data_xml_dialog")

	data_xml_dialog = glade_xml_object.get_widget ("data_xml_dialog")
	data_entry = glade_xml_object.get_widget ("data_entry")
	textview = glade_xml_object.get_widget ("textview")
	
	if replace:
		out_fd = open (output_file, 'w')
		out_fd.write ("")
		out_fd.close ()
		
	out_fd = open (output_file, 'a')
	out_fd.write ('<?xml version="1.0"?>\n')
	out_fd.write ('<data>\n')

	button_close = glade_xml_object.get_widget ("button_close")
	button_close.connect ("clicked", close_dialog, data_xml_dialog, out_fd)

	button_clear = glade_xml_object.get_widget ("button_clear")
	button_clear.connect ("clicked", clear_fields, data_entry, textview)

	button_add = glade_xml_object.get_widget ("button_add")
	button_add.connect ("clicked", add_data_field, data_xml_dialog, data_entry, textview, out_fd)

def close_dialog (button, dialog, out_fd):
	out_fd.write ('</data>\n')
	out_fd.close()

	dialog.destroy()

def add_data_field (button, dialog, data_entry, textview, out_fd):
	data_name = data_entry.get_text()

	textbuffer = textview.get_buffer()	
	data_value = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), True)

	if data_name and data_name != " ":
		text = '  <' + data_name + '>' + data_value + '</' + data_name + '>\n'
		out_fd.write(text)

		message_dialog (dialog, gtk.MESSAGE_INFO, 'One data entry has been added to the XML data file.')
		clear_fields (None, data_entry, textview)
	else:
		message_dialog (dialog, gtk.MESSAGE_ERROR, 'Enter valid data in all fields.')

def clear_fields (button, entry, text_view):
	textbuffer = text_view.get_buffer()
	textbuffer.set_text("")

	entry.set_text("")
	entry.grab_focus()

def message_dialog (parent, flag, message):
	markup_message = '<big><b>' + message + '</b></big>'
	dialog = gtk.MessageDialog (parent, 0, flag, gtk.BUTTONS_OK, None)
	dialog.set_markup (markup_message)

	response = dialog.run ()
	if response:
		dialog.destroy ()
	
