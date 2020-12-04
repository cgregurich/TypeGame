from tkinter import *
import random
from colors import *
from timer import Timer
import PIL
from PIL import Image, ImageTk


# TODO:
# - Settings (change time, lines, chars per line, change words file/text, font??)

FONT = ("Consolas", 16)
STOPPED = "stopped"

class TypeGame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.TIME = 60

		# Display settings
		self.MAX_CHARS = 50 # number of characters allowed per line
		self.LINE_COUNT = 2 # number of lines that will display

		self.timer_status = BooleanVar()
		

		self.is_running = False
		self.typed_word = StringVar()

		# Logic setup
		self.words = {}
		self.init_words()
		self.word_index = 0
		self.goal_word = self.words[0][0]
		

		self.cursor = "1.0"
		self.cursor_end = "0.0"
		


		self.is_correct = False

		self.tags = []

		self.attempted_chars = 0
		self.correct_chars = 0
		self.attempted_words = 0
		self.correct_words = 0

		# Tkinter setup
		self.grid_columnconfigure(0, weight=1)

		LOWER_PADX = 10

		self.frame_words = Frame(self)
		self.frame_lower = Frame(self)
		
		self.entry = Entry(self.frame_lower, font=FONT, textvariable=self.typed_word, bd=1, relief=SOLID)
		

		self.text_display = Text(self.frame_words, font=FONT, height=2)

		self.entry.bind("<KeyPress>", self.process_key_event)
		self.entry.bind("<KeyRelease>", self.process_key_event)

		self.entry.bind("<Control-BackSpace>", self.clear_typed)

		self.img_restart = None
		self.reset_btn = Button(self.frame_lower, relief=SOLID, bd=0, command=self.reset)

		self.img_settings = None
		self.settings_btn = Button(self.frame_lower, relief=SOLID, bd=0, command=self.open_settings)
		self.apply_button_images()


		self.results_text = Text(self.frame_lower, font=FONT, height=3, width=30, 
				bg=self.cget("bg"), relief=SOLID, bd=0, state=DISABLED)
		self.reset_results_text()

		self.results_text.grid(row=1, column=0, columnspan=3)

		self.text_display.config(height=self.LINE_COUNT, width=self.MAX_CHARS+10)



		# Timer setup
		m, s = divmod(self.TIME, 60)
		self.timer_lbl = Label(self.frame_lower, font=FONT)
		self.reset_timer_label()
		self.timer_id = None

		self.set_cursor_end()
		self.draw_words()
		self.highlight_goal_word()
		

		

		self.entry.focus()

		self.ctrl_down = False

		# Tkinter gridding
		self.frame_words.grid(row=0, column=0, padx=20)
		self.frame_lower.grid(row=1, column=0, padx=20)

		self.text_display.grid(row=0, column=1, padx=LOWER_PADX)

		self.settings_btn.grid(row=0, column=0, padx=LOWER_PADX)
		self.entry.grid(row=0, column=1, padx=LOWER_PADX)
		self.timer_lbl.grid(row=0, column=2)
		self.reset_btn.grid(row=0, column=3, padx=LOWER_PADX)
		Button(self, text="Test", command=self.test).grid(row=2, column=0)

	def open_settings(self):
		self.controller.show_frame("Settings")


	def apply_button_images(self):
		IMG_SIZE = 30
		img = Image.open("resources/restart.png")
		img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
		self.img_restart = ImageTk.PhotoImage(img)
		self.reset_btn.config(image=self.img_restart)

		img = Image.open("resources/settings.png")
		img = img.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
		self.img_settings = ImageTk.PhotoImage(img)
		self.settings_btn.config(image=self.img_settings)

		


	def set_results_text(self):

		# Set WPM, accuracy, correct words, wrong words, correct chars, wrong chars, total chars
		wpm = self.calc_wpm()
		accuracy = self.calc_accuracy()
		wrong_words = self.attempted_words - self.correct_words
		wrong_chars = self.attempted_chars - self.correct_chars
		self.results_text.config(state=NORMAL)
		self.results_text.delete("0.0", END)

		# WPM and ACCURACY
		self.results_text.insert(INSERT, f"{wpm} WPM")
		self.results_text.tag_add("wpm", "1.0", INSERT)
		
		self.results_text.insert(INSERT, f"   {accuracy}% accuracy\n")

		# WORDS
		self.results_text.insert(INSERT, "Words: ")
		start = self.results_text.index(INSERT)
		self.results_text.insert(start, f"{self.correct_words}")
		end = self.results_text.index(INSERT)
		self.results_text.tag_add("cw", start, end)
		self.results_text.insert(INSERT, f"|")
		start = self.results_text.index(INSERT)
		self.results_text.insert(start, f"{wrong_words}")
		end = self.results_text.index(INSERT)
		self.results_text.tag_add("ww", start, end)

		# KEYSTROKES
		self.results_text.insert(INSERT, "\n")
		self.results_text.insert(INSERT, "Keystrokes: ")
		start = self.results_text.index(INSERT)
		self.results_text.insert(INSERT, f"{self.correct_chars}")
		end = self.results_text.index(INSERT)
		self.results_text.tag_add("cks", start, end)
		self.results_text.insert(INSERT, "|")
		start = self.results_text.index(INSERT)
		self.results_text.insert(start, f"{wrong_chars}")
		end = self.results_text.index(INSERT)
		self.results_text.tag_add("wks", start, end)

		self.results_text.tag_config("cw", foreground="green")
		self.results_text.tag_config("ww", foreground="red")
		self.results_text.tag_config("wpm", foreground="green")
		self.results_text.tag_config("cks", foreground="green")
		self.results_text.tag_config("wks", foreground="red")


		self.results_text.config(state=DISABLED)
		
	def _get_col_from_results_text(self):
		return int(self.results_text.index(INSERT).split(".")[1])


	def reset_timer_label(self):
		"""Makes timer display the time before it starts counting down"""
		m, s = divmod(self.TIME, 60)
		self.timer_lbl.config(text="{}:{:02}".format(m, s))

	def reset(self):
		self.init_words()
		self.draw_words()
		self.reset_goal_word()
		self.unpause_input()
		self.reset_cursor()
		self.set_cursor_end()
		self.tags = []
		
		self.clear_bg_tag()
		self.highlight_goal_word()
		self.reset_word_data()
		self.reset_timer_label()
		self.reset_results_text()
		self.reset_timer()

	def reset_timer(self):
		if not self.timer_id:
			return
		self.after_cancel(self.timer_id)
		self.is_running = False
		

	def reset_word_data(self):
		self.attempted_chars = 0
		self.correct_chars = 0
		self.attempted_words = 0
		self.correct_words = 0


	def clear_bg_tag(self):
		self.text_display.tag_delete("bg")

	def reset_goal_word(self):
		"""Resets goal word to the 0th element in self.words[0]
		and sets word_index to 0"""
		self.goal_word = self.words[0][0] 
		self.word_index = 0

	def reset_results_text(self):
		self.results_text.config(stat=NORMAL)
		self.results_text.delete("0.0", END)
		self.results_text.insert(INSERT, "\nFinish typing to get results.")
		self.results_text.config(stat=DISABLED)

	def clear_typed(self, event):
		self.entry.delete(0, END)


	def start_timer(self):
		self.timer_loop(self.TIME)

	def timer_loop(self, seconds):
		"""seconds is the grand total number of seconds left in the timer"""
		m, s = divmod(seconds, 60)
		# Continue looping if timer is not done
		x = 0

		if seconds != 0:
			self.time_left = seconds
			if self.is_running == True:
				self._redraw_clock_label(m, s)
				x = 1
			self.timer_id = self.after(1000, self.timer_loop, seconds - x)
		else:
			self.is_running = False
			self._redraw_clock_label(0, 0)
			self.set_results_text()
			self.pause_input()

	def pause_input(self):
		self.entry.delete(0, END)
		self.entry.config(state=DISABLED)
		self.focus()

	def unpause_input(self):
		self.entry.config(state=NORMAL)
		self.entry.focus()

	def _redraw_clock_label(self, m, s):
		self.timer_lbl.config(text="{}:{:02}".format(m, s))


	def init_words(self):
		self.words = {line:[] for line in range(self.LINE_COUNT)}
		for line in self.words.keys():
			self.words[line] = self.generate_words_list()

	def get_all_words(self):
		with open("resources/words.txt", "r") as file:
			words = file.read().split("|")
		return words

	def random_word(self):
		return random.choice(self.get_all_words())

	def test(self):
		print(self.results_text.tag_names("2.7"))
		print(self.results_text.tag_names("1.0"))

	def draw_words(self):
		"""Draws all the words to be displayed in the Text widget"""
		self.text_display.config(state=NORMAL)
		self.text_display.delete("0.0", END)
		for line_num, words_list in self.words.items():
			for i, word in enumerate(words_list):
				self.text_display.insert(INSERT, word)

				if i != len(words_list) - 1:
					self.text_display.insert(INSERT, " ")
				
			if line_num < self.LINE_COUNT - 1:
				self.text_display.insert(INSERT, "\n")
		self.text_display.config(state=DISABLED)

	def check_typed(self):
		"""Returns true if the typed word before the space matches the goal word, 
		else returns false"""
		self.is_correct = self.typed_word.get() == self.goal_word
		return self.is_correct

	def next_word(self):
		"""Clears entry, clears typed word, increments goal word index,
		redraws word prompts, and sets goal word to next word"""


		self.mark_word()
		self.increment_cursor()
		self.word_index += 1

		# Check if we're at last word of the line
		if self.word_index == len(self.words[0]):
			self.next_line()

		self.goal_word = self.words[0][self.word_index]
		self.set_cursor_end()
		self.entry.delete(0, END)

		self.highlight_goal_word()

	def mark_word(self):
		# Mark the current goal word; this func is called
		# when user enters space and moves to next word, but 
		# before the cursor moves to the next word
		tag_name = f"tag{len(self.tags)}"
		self.tags.append(tag_name)
		self.text_display.tag_add(tag_name, self.cursor, self.cursor_end)
 
		color = "green" if self.is_correct else "red"
		self.text_display.tag_config(tag_name, foreground=color)

	def increment_cursor(self):
		"""Sets cursor to start of next word"""
		word_len = len(self.goal_word)
		row = self.cursor.split(".")[0]
		column = self.cursor.split(".")[1]
		self.cursor = f"{row}.{int(column) + word_len + 1}"

	def set_cursor_end(self):
		word_len = len(self.goal_word)
		row = self.cursor.split(".")[0]
		column = self.cursor.split(".")[1]
		self.cursor_end = f"{row}.{int(column) + word_len}"

	def reset_cursor(self):
		self.cursor = "1.0"
		
	def highlight_goal_word(self):
		self.text_display.tag_delete("bg")
		self.text_display.tag_add("bg", self.cursor, self.cursor_end)
		self.text_display.tag_config("bg", background=GREY)

	def next_line(self):
		# Replace first line with second line
		self.words[0] = self.words[1]
		# Shift all lines up one
		self.shift_lines_up()
		# Create new bottom line
		self.words[self.LINE_COUNT - 1] = self.generate_words_list()
		# Draw new lines to screen
		self.draw_words()
		# Reset word index
		self.word_index = 0
		# Reset curors
		self.reset_cursor()
		self.set_cursor_end()
		# Clear tags
		self.tags = []


	def shift_lines_up(self):
		new_words = {i: [] for i in range(self.LINE_COUNT)}
		for i in range(1, self.LINE_COUNT):
			new_words[i-1] = self.words[i]
		self.words = new_words



	def generate_words_list(self):
		"""Generate and return a list of words that fit within 
		the given number of characters per line"""
		line_chars = 0
		words_list = []
		while line_chars <= self.MAX_CHARS:
			new_word = self.random_word()
			if line_chars + len(new_word) + 1 > self.MAX_CHARS:
				if line_chars + len(new_word) > self.MAX_CHARS:
					break
				else:
					words_list.append(new_word)
					line_chars += len(new_word)
					continue
			words_list.append(new_word)
			line_chars += len(new_word) + 1
		return words_list

	def process_key_event(self, event):
		# types: 2 = press, 3 = release
		if self.is_running == False:
			self.is_running = True
			self.start_timer()
		if event.char == " ":
			self.process_space(event)

		# Keep track of ctrl state
		# if event.keysym == "Control_L" or event.keysym == "Control_R":
		# 	if event.type == "2":
		# 		self.ctrl_down = True
		# 	if event.type == "3":
		# 		self.ctrl_down = False
		# # ctrl + backspace should remove the entire word
		# if event.keysym == "BackSpace" and self.ctrl_down:
		# 	self.entry.delete(0, END)

	def process_space(self, event):
		"""If space is pressed, then clear the entry.
		If space is released, then clear the first character in the entry, 
		which would be the space that is input after the previous space KeyPress event.
		Because the space isn't sent to the entry until AFTER the KeyPress event is processed
		in process_key_event()"""

		if event.type == "2": # Press
			self.check_typed()
			self.increment_word_data()
			if self.typed_word.get():
				self.next_word()
			self.entry.delete(0, END)
		elif event.type == "3": # Release
			self.entry.delete(0, 1)

	def increment_word_data(self):
		self.attempted_words += 1
		self.attempted_chars += len(self.goal_word) + 1
		if self.is_correct:
			self.correct_chars += len(self.goal_word) + 1
			self.correct_words += 1
		else:
			self.correct_chars += 1 # for the space

		
	

	def calc_wpm(self):
		if self.attempted_chars == 0:
			return 0
		wpm = round((self.correct_chars / 5) / (self.TIME / 60))
		return wpm

	def calc_accuracy(self):
		if self.attempted_chars == 0:
			return 0
		accuracy = (round((self.correct_chars / self.attempted_chars) * 1000)) / 10
		return accuracy

	

if __name__ == "__main__":
	tg = TypeGame()
	tg.mainloop()