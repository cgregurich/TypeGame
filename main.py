from tkinter import *
from typegame import TypeGame
from settings import Settings


class MainApp(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		self.geometry("675x200")

		self.title("Booter Type")

		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for gui_class in (TypeGame, Settings):
			frame = gui_class(container, self)
			self.frames[gui_class.__name__] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("TypeGame")

	def show_frame(self, gui_class):
		frame = self.frames[gui_class]
		frame.tkraise()

def main():
	MainApp().mainloop()

if __name__ == "__main__":
	main()

