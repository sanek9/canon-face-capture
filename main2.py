#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
#from SimpleCV import Camera
import face_recognition
import numpy as np

import gphoto2 as gp
class BackGroundSubtractor:
	# When constructing background subtractor, we
	# take in two arguments:
	# 1) alpha: The background learning factor, its value should
	# be between 0 and 1. The higher the value, the more quickly
	# your program learns the changes in the background. Therefore, 
	# for a static background use a lower value, like 0.001. But if 
	# your background has moving trees and stuff, use a higher value,
	# maybe start with 0.01.
	# 2) firstFrame: This is the first frame from the video/webcam.
	def __init__(self,alpha,firstFrame):
		self.alpha  = alpha
		self.backGroundModel = firstFrame

	def getForeground(self,frame):
		# apply the background averaging formula:
		# NEW_BACKGROUND = CURRENT_FRAME * ALPHA + OLD_BACKGROUND * (1 - APLHA)
		self.backGroundModel =  frame * self.alpha + self.backGroundModel * (1 - self.alpha)

		# after the previous operation, the dtype of
		# self.backGroundModel will be changed to a float type
		# therefore we do not pass it to cv2.absdiff directly,
		# instead we acquire a copy of it in the uint8 dtype
		# and pass that to absdiff.

		return cv2.absdiff(self.backGroundModel.astype(np.uint8),frame)

	
class Camera:
    def open(self):
	self.cam = cv2.VideoCapture(0)
	ret, frame = self.cam.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	self.cam.release()
#	self.camera = gp.check_result(gp.gp_camera_new())
#	gp.check_result(gp.gp_camera_init(self.camera))
    def close(self):
	del(self.cam)

    def capture(self):
	self.cam = cv2.VideoCapture(0)
	ret, frame = self.cam.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	self.cam.release()
	return frame

class CannonCamera:
    def open(self):
	
	self.camera = gp.check_result(gp.gp_camera_new())
	gp.check_result(gp.gp_camera_init(self.camera))
    def close():
	gp.check_result(gp.gp_camera_exit(self.camera))
    def capture(self):
	print('Capturing image')
    	file_path = gp.check_result(gp.gp_camera_capture(
        self.camera, gp.GP_CAPTURE_IMAGE))
    	print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
   	target = os.path.join('/tmp', file_path.name)
	print('Copying image to', target)
	camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
	gp.check_result(gp.gp_file_save(camera_file, target))

	color = Image.open(target)
	img = np.array(color, 'uint8')
	return img
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
	self.cam = Camera()
	self.backSubtractor = BackGroundSubtractor(0.01,self.denoise(self.cam.capture()))
    def on_MainWindow_delete_event(self, widget, event):
	self.cam.close()
        Gtk.main_quit()
	
    def denoise(self,frame):
	frame = cv2.medianBlur(frame,5)
	frame = cv2.GaussianBlur(frame,(5,5),0)
	return frame
    def background(self, button):
	print("click")
	self.backgroud = self.cam.capture()
	self.backSubtractor = BackGroundSubtractor(0.01,self.denoise(self.backgroud))
	
    def capture(self, button):
	greyscale = False
	frame = self.cam.capture()
	
	#frame = cv2.resize(frame, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#	frame = cv2.sub(frame, self.backgroud)
	foreGround = self.backSubtractor.getForeground(self.denoise(frame))
	ret, mask = cv2.threshold(foreGround, 15, 255, cv2.THRESH_BINARY)
	mask = cv2.convertScaleAbs(mask)
	mask = cv2.cvtColor(mask,cv2.COLOR_RGB2GRAY)
	face_locations = face_recognition.face_locations(frame)
	


	mask_inv = cv2.bitwise_not(mask)

	white = np.ones(frame.shape, frame.dtype)*255
	white = cv2.bitwise_and(white,white,mask = mask_inv)

	
	fg = cv2.bitwise_and(frame, frame, mask=mask)
	res = cv2.add(fg,white)

	res = self.denoise(res)
#	res = cv2.medianBlur(res,11)
#	res = cv2.GaussianBlur(res,(7,7),0)
#	res = cv2.bitwise_and(res,res,mask = mask_inv)
#	res = cv2.add(fg,res)

	for face in face_locations:
		(y1, x2, y2, x1) = face
#		ratio = 15.0/21.0
#		scale = 1.3
		
		width = x2-x1
		hight = y2-y1
		fx1 = int(x1-width*0.5)
		fx2 = int(x2+width*0.5)
		fy1 = int(y1-hight*0.6)
#		fy2 = int((fx2-fx1)*(4/3))		
		fy2 = int(y2+hight*0.8)
		fw = fx2-fx1
		fh = fy2-fy1
		print(str(fw)+' '+str(fh)+' '+str(fw/fh))
		cv2.rectangle(res, (x1, y1), (x2, y2), (0, 0, 255), 2)
		cv2.rectangle(res, (fx1, fy1), (fx2, fy2), (0, 0, 255), 2)
		print(face)
	
	pb = GdkPixbuf.Pixbuf.new_from_data(res.tostring(),
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
	self.cam.open()
	self.backgroud = self.cam.capture()
	print("click2")

if __name__ == "__main__":
    try:
        win = HellowWorldGTK()
#	win.connect("delete-event", Gtk.main_quit)
#	win.show_all()
	Gtk.main()
    except KeyboardInterrupt:
        pass


