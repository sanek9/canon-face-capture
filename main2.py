#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
#from SimpleCV import Camera
import face_recognition
class HellowWorldGTK:

    def __init__(self):
#	Gtk.Window.__init__(self, title="Hello World")
        self.gladefile = "pyhelloworld.glade"
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)
	self.image_view = self.glade.get_object("image")
        self.glade.connect_signals(self)
        self.win = self.glade.get_object("MainWindow")
#	self.add(self.win)
	self.win.connect("delete-event", self.on_MainWindow_delete_event)
	self.win.show_all()

    def on_MainWindow_delete_event(self, widget, event):
	del(self.cam)
        Gtk.main_quit()
    def capture1(self, button):
	print("click")
#	img = cam.getImage()
	return_value, img = self.cam.read()
	print(type(img))
	print(type(return_value))
#	print(img)
#	print(dir(img))
#	print(img.size)
#	print(img[0].size)
#	print(img[1].size)
#	cv2.imshow('frame',img)
	h, w, d = img.shape
	pixbuf = GdkPixbuf.Pixbuf.new_from_data  (img.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*3, None, None)
	self.image_view.set_from_pixbuf (pixbuf.copy())
	
	
    def capture(self, button):
	greyscale = False
	self.cam = cv2.VideoCapture(0)
	ret, frame = self.cam.read()
	self.cam.release()
	#frame = cv2.resize(frame, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#	if greyscale:
#		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
#	else:
#		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	face_locations = face_recognition.face_locations(frame)
	for face in face_locations:
		(top, right, bottom, left) = face
#		top *= 4
#		right *= 4
#		bottom *= 4
#		left *= 4

		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
		print(face)

#	cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
	pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
		                        GdkPixbuf.Colorspace.RGB,
		                        False,
		                        8,
		                        frame.shape[1],
		                        frame.shape[0],
		                        frame.shape[2]*frame.shape[1])
	self.image_view.set_from_pixbuf(pb.copy())

    def face_cut(self, img):

	print("some")

    def open(self, button):
#	self.cam = cv2.VideoCapture(0)
#	self.cam = Camera()
	print("click2")

if __name__ == "__main__":
    try:
        win = HellowWorldGTK()
#	win.connect("delete-event", Gtk.main_quit)
#	win.show_all()
	Gtk.main()
    except KeyboardInterrupt:
        pass


