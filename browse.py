import gtk

def dir_ok_sel(default, filew, entry1):
	entry1.set_text (filew.get_filename ())	
	filew.destroy()

def close_dialog(default, filew):
	filew.destroy()

def select_dir(default, entry1):
	filew = gtk.FileSelection ('Open File ...')
	filew.file_list.hide ()
	filew.connect("destroy", close_dialog, filew)
	filew.ok_button.connect("clicked", dir_ok_sel, filew, entry1)
	filew.cancel_button.connect("clicked", close_dialog, filew)
	filew.show()	

