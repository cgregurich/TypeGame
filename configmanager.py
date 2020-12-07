import configparser

class ConfigManager(configparser.ConfigParser):
	def __init__(self):
		super().__init__(self)

		self.FILE_NAME = "config.ini"
		self.check_for_config_file()

	def check_for_config_file(self):
		if not self.read(self.FILE_NAME):
			self.create_config_file()
		

	def create_config_file(self):
		self["SETTINGS"] = {"Time": "60", "WordsFile": "words.txt"}
		with open(self.FILE_NAME, "w") as file:
			self.write(file)

	def change_setting(self, section, key, value):
		self.set(section, key, value)
		with open(self.FILE_NAME, "w") as configfile:
			self.write(configfile)

	def get_setting(self, section, option):
		self.read(self.FILE_NAME)
		value = self[section][option]
		return value



		