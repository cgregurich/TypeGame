from tkinter import *

# WHERE I LEFT OFF:
# Got the editor saving to work (add ctrl+s bind??)
# Had to fix the Text widget's default behavior of adding a '\n' to the end of the text

# What do we want out of the settings?

# Change the time on the timer
# Change the line count? 
# Change the characters allowed per line?
# access the list of words that are pulled (i.e. words.txt) Open this in a text widget?

# TODO
# - how to init editor in __init__ without it popping up???
# - draw current file in Text widget
# - have editor window pop up when button clicked
# - only one instance of editor allowed
# - check for changes when x'd out
# - if main program is x'd, then close editor as well
# - disable main program when editor is open


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

		self.editor = None
		self.editor_text = None

		
	def draw_settings(self):
		settings = (("time", "time"), ("wordsfile", "words file"))
		row = 0
		for s in settings:
			Label(self.options_frame, text=s[1].title(), font=FONT).grid(row=row, column=0)
			if s[0] == "wordsfile":
				temp_frame = Frame(self.options_frame)
				temp_frame.grid(row=row, column=1)
				Button(temp_frame, text="Edit", font=FONT, command=self.edit_file).grid(row=0, column=0, padx=10)
				Button(temp_frame, text="Default", font=FONT, command=self.reset_file).grid(row=0, column=1, padx=10)
				
			else:
				# draw a label and then an appropriate widget to modify the option
				
				e = Entry(self.options_frame, font=FONT)
				e.grid(row=row, column=1)
				self.entries[s[0]] = e
				e.insert(0, self.cfgmgr.get_setting("SETTINGS", s[0]))
			row += 1
		# Button(self.options_frame, text="Save", font=FONT, command=self.save_clicked).grid(row=row, column=0, columnspan=2,
		# 			pady=10)

	def reset_file(self):
		with open("resources/default_words.txt", "r") as file:
			default_words = file.read()
		with open("resources/words.txt", "w") as file:
			file.write(default_words)

	def save_clicked(self):
		self.save_settings()
		


	def save_settings(self):
		for name, entry in self.entries.items():
			self.cfgmgr.change_setting("SETTINGS", name.title(), entry.get())

	def back_clicked(self):
		self.save_settings()
		self.controller.show_frame("TypeGame")


	def edit_file(self):
		self.editor = Toplevel()
		self.editor_text = Text(self.editor, font=FONT)
		self.editor_text.grid(row=0, column=0)
		button_frame = Frame(self.editor)
		button_frame.grid(row=1, column=0)
		Button(button_frame, text="Save", font=FONT, command=self.save_editor).grid(row=0, column=0)

		

		with open("resources/words.txt", "r") as file:
			words = file.read()
		
		
		self.editor_text.insert(INSERT, words)

	def save_editor(self):
		contents = self.editor_text.get("0.0", END)

		with open("resources/words.txt", "w") as file:
			file.write(contents[:len(contents)-1])

		self.editor.destroy()