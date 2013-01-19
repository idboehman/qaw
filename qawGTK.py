#!/usr/bin/python

'''  
    Morgan Phillips (c) 2013

    This file is part of qaw.

    qaw is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    qaw is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with qaw.  If not, see <http://www.gnu.org/licenses/>.
'''

import pygtk
pygtk.require('2.0')
import gtk

from qawlibs import qaexceptions,qabackend

class QAWGTK:

    def qaMain(self, widget, data=None):
        print "GTK Version Coming Soon!"

    def delete_event(self, widget, event, data=None):
        print "Goodbye...."
	return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        
	self.button = gtk.Button("Nothing to see yet....")
        self.button.connect("clicked", self.qaMain, None)
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
    
        self.window.add(self.button)
        self.button.show()
        self.window.show()

    def main(self):
        gtk.main()

qawGUISession = QAWGTK()
qawGUISession.main()
