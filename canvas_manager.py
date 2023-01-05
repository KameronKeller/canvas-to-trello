from commandline_printer import CommandLinePrinter as printer
from canvasapi import Canvas

class CanvasManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager
		self.canvas_client = Canvas(None, None)

	def interactive_setup(self):
		printer.print_divider("Canvas Setup")
		canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
		self.config_manager.update_config('canvas', 'url', canvas_api_url)
		self.config_manager.update_config('canvas', 'api_key', "")
		self.canvas_client = Canvas(canvas_api_url, None)

	def create_course_map(self):
		user = canvas_client.get_current_user()
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
			course_number = get_course_number(name)

			term = get_term(name)

			# Both a course number and term number are required
			if course_number and term:
				course_map[course_number] = {"course" : course, "term" : term}
		return course_map
