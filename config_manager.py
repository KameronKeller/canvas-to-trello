import configparser

class ConfigManager:

	def __init__(self, config_file='config.ini'):
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

	def load_config(self):
		self.config_parser.read(self.config_file)

	def get_configuration(self, section, attribute):
		self.load_config()
		return self.config_parser[section][attribute]

	def get_boolean(self, section, attribute):
		self.load_config()
		return self.config_parser[section].getboolean(attribute)

	def has_option(self, section, attribute):
		return self.config_parser.has_option(section, attribute)

	def setup_complete(self):
		try:
			return self.get_boolean('setup', 'setup_complete')
		except KeyError:
			return False



