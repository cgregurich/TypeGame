from tkinter import *

# WHERE I LEFT OFF:
# getting the .ini and config shish up and running. currently making the func
# init config and draw settings and shish

# What do we want out of the settings?

# Change the time on the timer
# Change the line count? 
# Change the characters allowed per line?
# access the list of words that are pulled (i.e. words.txt) Open this in a text widget?

from configmanager import ConfigManager

FONT = ("Consolas", 16)

class Settings(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		# change this to an arrow or something probably
		Button(self, text="Back", command=self.back_clicked).grid(row=0, column=0) 
		self.options_frame = Frame(self)
		self.options_frame.grid(row=1, column=1)

		self.entries = {}

		self.cfgmgr = ConfigManager()
		self.draw_settings()



		


	def draw_settings(self):
		settings = (("time", "time"), ("wordsfile", "words file"), ("linecount", "line count"), 
						("maxcharsperline", "max chars per line"))
		row = 0
		for s in settings:
			# draw a label and then an appropriate widget to modify the option
			Label(self.options_frame, text=s[1].title(), font=FONT).grid(row=row, column=0)
			e = Entry(self.options_frame, font=FONT)
			e.grid(row=row, column=1)
			self.entries[s[0]] = e
			e.insert(0, self.cfgmgr.get_setting("SETTINGS", s[0]))
			row += 1
		Button(self.options_frame, text="Save", font=FONT, command=self.save_clicked).grid(row=row, column=0, columnspan=2)

	def save_clicked(self):
		self.save_settings()

	def save_settings(self):
		for name, entry in self.entries.items():
			self.cfgmgr.change_setting("SETTINGS", name.title(), entry.get())
			print(f"change setting {name}")

		


	def back_clicked(self):
		self.controller.show_frame("TypeGame")

