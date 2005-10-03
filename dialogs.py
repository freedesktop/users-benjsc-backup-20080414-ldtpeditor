import gtk

def file_dialog (title, parent, action, multiple_selection=False, default_file=None):
	if action == gtk.FILE_CHOOSER_ACTION_SAVE:
		buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			   gtk.STOCK_SAVE, gtk.RESPONSE_OK)
	else:
		buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			   gtk.STOCK_OPEN, gtk.RESPONSE_OK)

	dialog = gtk.FileChooserDialog (title, parent, action, buttons)

	if multiple_selection:
		dialog.set_select_multiple (multiple_selection)

	if default_file:
		dialog.set_current_name (default_file)

	dialog.set_default_response (gtk.RESPONSE_OK)
	return dialog

def message_dialog (parent, message_type, buttons, default_response, primary_text, secondary_text=None):
	dialog = gtk.MessageDialog (parent, 0, message_type, gtk.BUTTONS_NONE, None)
	i = 0

	while i < len(buttons):
		button_text = buttons[i]
		response_id = buttons[i+1]
		dialog.add_button (button_text, response_id)
		i = i+2
		
	dialog.set_markup ('<big><b>' + primary_text + '</b></big>')

	if secondary_text:
		dialog.format_secondary_text (secondary_text)
		
	dialog.set_default_response (default_response)

	return dialog
