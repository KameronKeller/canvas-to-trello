import configparser

class ConfigManager:

	def __init__(self, config_file):
		self.config_file = config_file
		self.config_parser = configparser.ConfigParser()

	def write(self):
		with open(self.config_file, 'w') as file:
			self.config_parser.write(file)

	def add_config_section(self, name):
		self.config_parser[name] = {}
		self.write()

	def update_config(self, section, attribute, value):
		self.config_parser[section][attribute] = value
		self.write()


