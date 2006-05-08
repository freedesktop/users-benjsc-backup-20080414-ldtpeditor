#!/usr/bin/env python

#
# Linux Desktop Testing Project http://www.gnomebangalore.org/ldtp
#
# Author:
# 	Shankar Ganesh(shagan.glare@gmail.com)
#	Harishankaran (sp2hari@gmail.com)
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
import gtk, browse
from time import *
try:
	import commands,os,sys,gobject,time
except ImportError:
        print 'Python-commands package not installed'

def close_dialog (p, dialog):
	dialog.destroy ()
	cmd = "kill -s TERM `pidof record`"

def callback(source, condition):
	if (condition & (gobject.IO_HUP | gobject.IO_ERR)):
		print "error"
		return False
	else:
		print "hello"
		print os.read(source,100)
		return True
                                                                                                                             
def toggle_button_callback(widget,data,entry,entry1):
      if widget.get_active():
	widget.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("#ff0000"))
	widget.set_label("STOP")
	pid=os.fork()
	if pid==0:
		cmd = "record -a " + entry.get_text() + " -f " + entry1.get_text() + " -e "
		print cmd
		status = commands.getstatusoutput(cmd)
		print status
	       	if status[0] != 0:
        	        print "Unable to Run Recording"
			#FIX ME : Getting Leakage Err every time record is closed
			sys.exit(0)
		sys.exit(0)
	else:
		print os.getcwd()
		sleep(2)
		fp =os.open('/tmp/FromC',os.O_NONBLOCK,0777)
		gobject.io_add_watch(fp,gobject.IO_IN,callback)
      else:
	widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#00ff00"))
	widget.set_label("START")
	cmd = "kill -s TERM `pidof record`"
        status = commands.getstatusoutput(cmd)
        if status[0] != 0:
                print "Unable to kill Recording"
	return True
            
                                                                                                                            
def recorder ():
	dialog = gtk.Dialog()
	dialog.set_size_request(330, 180)
	dialog.set_title ("Recording")
	dialog.connect ("destroy", close_dialog, dialog)

	label = gtk.Label ("Name             ")
	label.show ()

	global entry
	entry = gtk.Entry ()
	box = gtk.HBox ()
	box.pack_start (label, gtk.FALSE, gtk.FALSE, 0)
	box.pack_start (entry, gtk.FALSE, gtk.FALSE, 0)
	entry.show ()
	box.show ()

	label_fill = gtk.Label ("                ")
	label_fill.show ()
	label_fill_1 = gtk.Label ("           ")
	label_fill_1.show ()
	label_fill_2 = gtk.Label ("           ")
	label_fill_2.show ()
	label = gtk.Label ("Output file        ")
	label.show ()
	entry1 = gtk.Entry ()
	entry1.show ()
	button = gtk.Button ('Browse...')
	button.connect_object ('clicked', browse.select_dir, dialog, entry1)
	button.show ()
	box1 = gtk.HBox ()
	box1.pack_start (label, gtk.FALSE, gtk.FALSE, 0)
	box1.pack_start (entry1, gtk.FALSE, gtk.FALSE, 0)
	box1.pack_start (button, gtk.FALSE, gtk.FALSE, 0)
	box1.show ()
	label = gtk.Label ("Recording             ")
	label.show ()
	toggle_button = gtk.ToggleButton(label="START")
	toggle_button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#00ff00"))
	toggle_button.connect("clicked",toggle_button_callback,toggle_button,entry,entry1)
	toggle_button.set_mode(0)
        
	      
	box2 = gtk.HBox ()
	box2.pack_start (label, gtk.FALSE, gtk.FALSE, 0)
	box2.pack_start (toggle_button, gtk.FALSE, gtk.FALSE, 0)
	toggle_button.show ()
	box2.show ()
	
	vbox = gtk.VBox ()
	vbox.pack_start (label_fill_1, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start (box, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start (label_fill, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start (box1, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start (label_fill_2, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start (box2, gtk.FALSE, gtk.FALSE, 0)
	vbox.show ()

	dialog.vbox.pack_start (vbox, gtk.TRUE, gtk.TRUE, 0)
	
	quit_button=gtk.Button("Quit")
	quit_button.connect("clicked", close_dialog,dialog)
	dialog.action_area.pack_start(quit_button, gtk.TRUE, gtk.TRUE, 0)
	quit_button.show()
	
	dialog.show()

                                                                                                                             

