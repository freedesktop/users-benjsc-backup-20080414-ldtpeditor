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
