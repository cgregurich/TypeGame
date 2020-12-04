from tkinter import *

# WHERE I LEFT OFF:
# getting the .ini and config shish up and running. currently making the func
# init config and draw settings and shish

# What do we want out of the settings?

# Change the time on the timer
# Change the line count? 
# Change the characters allowed per line?
# access the list of words that are pulled (i.e. words.txt) Open this in a text widget?

import configparser


class Settings(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller


		Button(self, text="Back", command=self.back_clicked).grid(row=0, column=0) #chage this to an arrow or something probably
		Label(self, text="Settings Page").grid(row=0, column=1)

		self.cfg_p = configparse.ConfigParser()
		self.init_config()

	def 


	def draw_settings(self):


	def back_clicked(self):
		self.controller.show_frame("TypeGame")

