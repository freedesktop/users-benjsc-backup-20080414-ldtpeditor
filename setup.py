#!/usr/bin/python

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
