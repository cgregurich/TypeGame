import sqlite3


class ResultDAO():
	def __init__(self, db_name="results.db"):
		self.conn = sqlite3.connect(db_name)
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS results (
			seconds integer, wpm text, accuracy decimal, correct_words integer, 
			wrong_words integer, correct_ks integer, wrong_ks integer,
			time_completed text, date_completed text)""")

	def insert_result(self, result):
		with self.conn:
			self.c.execute("""INSERT INTO results VALUES(
				:seconds, :wpm, :accuracy, :correct_words, :wrong_words, :correct_ks,
				:wrong_ks, :time_completed, :date_completed
				)""", result.data)






	# Reference code from SessionDAO
	# def delete_session(self, session_to_del):
	# 	with self.conn:
	# 		self.c.execute("""DELETE FROM sessions WHERE 
	# 			task=? AND task_time=? AND time_completed=? AND date_completed=?""", ('reading', 120, '16:14', '8-22-2020'))
	# 		# session_to_del.info_as_tuple()
	# 	return self.c.rowcount


	# def get_all_sessions(self):
	# 	"""Pulls all data from database and uses helper to convert to and return
	# 	list of Session objects"""
	# 	with self.conn:
	# 		self.c.execute("""SELECT * FROM sessions ORDER BY date_completed, time_completed""")
	# 		tup_list = self.c.fetchall()

	# 	return self._convert_tup_list_to_session_list(tup_list)


	# def _convert_tup_list_to_session_list(self, tup_list):
	# 	"""Helper method for get_all_sessions. Receives a list of tuples 
	# 	and returns a list of Session objects"""
	# 	session_list = []

	# 	for tup in tup_list:
	# 		info_dict = {'task':tup[0], 'task_time':tup[1], 'time_completed':tup[2], 'date_completed':tup[3]}
	# 		s = Session()
	# 		s.set_info_from_dict(info_dict)
	# 		session_list.append(s)

	# 	return session_list

	# def get_all_sessions_from_date(self, date):
	# 	"""Arg date must be datetime.date object"""
	# 	all_sessions = self.get_all_sessions()
	# 	sessions_list = []
	# 	for session in all_sessions:
	# 		session_datetime_obj = session.get_date_obj()
	# 		if session_datetime_obj == date:
	# 			sessions_list.append(session)

	# 	return sessions_list

	# def get_all_sessions_between_dates(self, start, end):
	# 	"""Returns list of Session objects that have a date_completed on and between
	# 	start and end"""

	# 	dates = self._generate_dates_between(start, end)
	# 	sessions = []
	# 	for date in dates:
	# 		sessions += self.get_all_sessions_from_date(date)
	# 	return sessions



	# def _generate_dates_between(self, start, end):
	# 	"""Returns a list of date objects starting at start and ended on end"""
	# 	dates = []
	# 	temp = start
	# 	while temp <= end:
	# 		dates.append(temp)
	# 		temp += dt.timedelta(days=1)
	# 	return dates


	# def get_all_sessions_by_task(self, task):
	# 	"""ARG task : str"""
	# 	with self.conn:
	# 		self.c.execute("""SELECT * FROM sessions WHERE task = ?
	# 			ORDER BY date_completed, time_completed""", (task,))
	# 		tup_list = self.c.fetchall()

	# 	return self._convert_tup_list_to_session_list(tup_list)