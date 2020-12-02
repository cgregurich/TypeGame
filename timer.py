from tkinter import *

FONT = ("Consolas", 16)

STOPPED = "stopped"
RUNNING = "running"

class Timer(Frame):
	def __init__(self, parent, time, var):
		Frame.__init__(self, parent)

		self.time = time
		self.mode = STOPPED
		self.var = var
		self.parent = parent

		# Create sub-frames

		self.finished = True
	
		m, s = divmod(self.time, 60)

		self.lbl_time = Label(self, text="{}:{:02}".format(m, s), fg="black")
		# Have to config to override default BooterLabel options
		self.lbl_time.config(font=FONT)	

		self.timer_id = None
		self.lbl_time.grid(row=0, column=0)



	def start_timer(self, seconds):
		self.mode = RUNNING
		self.var.set(True)
		self.timer_loop(seconds)
		self.finished = False



	def timer_loop(self, seconds):
		"""seconds is the grand total number of seconds left in the timer"""
		m, s = divmod(seconds, 60)
		# Continue looping if timer is not done
		x = 0

		if seconds != 0:
			self.time_left = seconds
			if self.mode == RUNNING:
				self._redraw_clock_label(m, s)
				x = 1
			self.timer_id = self.after(1000, self.timer_loop, seconds - x)
		else:
			self.var.set(False)
			self.mode = STOPPED
			self._redraw_clock_label(0, 0)
			self.finished = True
			self.parent.calc_wpm()

	def _redraw_clock_label(self, m, s):
		self.lbl_time.config(text="{}:{:02}".format(m, s))

		


			


		
		



def main():
	timer = timer()
	timer.mainloop()


if __name__ == '__main__':
	main()
