#!/usr/bin/python

from distutils.core import setup

script_list = ('/usr/lib/ldtpeditor', ['ldtpeditor.py', 'dialogs.py', 'xmldatadialog.py', 'syntax.py'])
data_file_list = ('/usr/lib/ldtpeditor', ['data_xml.glade', 'log_file.glade', 'ldtp-logo-small.png'])

setup (name="ldtpedit",
       version="0.1.0",
       description="Editor for GNU/Linux Desktop Testing Project",
       author="Khasim Shaheed",
       author_email="sshaik@novell.com",
       url="http://gnomebangalore.org/ldtp",
       data_files=[script_list, data_file_list],
       scripts=['ldtpedit']
       )
