#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class HellowWorldGTK:

    def __init__(self):
#	Gtk.Window.__init__(self, title="Hello World")
        self.gladefile = "pyhelloworld.glade" 
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        self.win = self.glade.get_object("MainWindow")
#	self.add(self.win)
	self.win.connect("delete-event", Gtk.main_quit)
	self.win.show_all()

    def on_MainWindow_delete_event(self, widget, event):
        Gtk.main_quit()

if __name__ == "__main__":
    try:
        win = HellowWorldGTK()
#	win.connect("delete-event", Gtk.main_quit)
#	win.show_all()
	Gtk.main()
    except KeyboardInterrupt:
        pass
