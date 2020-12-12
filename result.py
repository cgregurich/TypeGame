

class Result:
	def __init__(self, data=None):
		"""Receives a dictionary of below format"""
		if data:
			self.data = data
		else:
			self.data = {"seconds": None,
					 "wpm": None,
					 "accuracy": None,
					 "correct_words": None,
					 "wrong_words": None,
					 "correct_ks": None,
					 "wrong_ks": None,
					 "time_completed": None,
					 "date_completed": None
					 }

				

	@property
	def seconds(self):
		return self.info["seconds"]

	@property
	def wpm(self):
		return self.info["wpm"]

	@property
	def accuracy(self):
		return self.info["accuracy"]

	@property
	def correct_words(self):
		return self.info["correct_words"]

	@property
	def wrong_words(self):
		return self.info["wrong_words"]

	@property
	def correct_ks(self):
		return self.info["correct_ks"]

	@property
	def wrong_ks(self):
		return self.info["wrong_ks"]

	@property
	def time_completed(self):
		return self.info["time_completed"]

	@property
	def date_completed(self):
		return self.info["date_completed"]

		