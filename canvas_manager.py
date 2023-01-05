import re
from commandline_printer import CommandLinePrinter as printer
from canvasapi import Canvas

class CanvasManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager
		self.time_format = '%Y-%m-%dT%H:%M:%SZ'
		try:
			self.config_manager.load_config()
			canvas_api_url = self.config_manager.get_configuration('canvas', 'url')
			canvas_api_key = self.config_manager.get_configuration('canvas', 'api_key')
			self.canvas_client = Canvas(canvas_api_url, canvas_api_key)
		except KeyError:
			print("Key not found in configuration. Was setup completed?")
			self.canvas_client = Canvas(None, None)

	def interactive_setup(self):
		printer.print_divider("Canvas Setup")
		canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
		self.config_manager.update_config('canvas', 'url', canvas_api_url)
		self.config_manager.update_config('canvas', 'api_key', "")
		self.canvas_client = Canvas(canvas_api_url, None)

	def create_course_map(self):
		user = self.canvas_client.get_current_user()
		courses = user.get_courses()
		course_map = {}
		for course in courses:
			try:
				# If the user assigned an alias for the course, get the original name
				if hasattr(course, "original_name"):
					name = course.original_name
				# Otherwise, get the default name
				else:
					name = course.name
			except AttributeError:
				continue

			# Get course code and section number
			course_number = self.get_course_number(name)

			term = self.get_term(name)

			start_at = course.start_at

			# Both a course number and term number are required
			if course_number and term:
				course_map[course_number] = {"course" : course, "term" : term, "start_at" : start_at}
		return course_map

	def get_course_number(self, name):
		# Returns the course number with the section number
		# Sample return = "CS_161_501"
		course_number_pattern = re.compile(r"\w{2}_\d{3}_\d{3}")
		course_number = course_number_pattern.search(name)
		if course_number:
			course_number = course_number.group(0)
		else:
			course_number = False
		return course_number

	def get_term(self, name):
		# Sample return: "F2022" AKA 'Fall 2022'
		term_pattern = re.compile(r"\w{1}\d{4}")
		term = term_pattern.search(name)
		if term:
			term = term.group(0)
		else:
			term = False
		return term
