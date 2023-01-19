import re
import ast
import datetime
from commandline_printer import CommandLinePrinter as printer
from canvasapi import Canvas
from simple_term_menu import TerminalMenu
from collections import defaultdict

class CanvasManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager
		self.time_format = '%Y-%m-%dT%H:%M:%SZ'
		if self.config_manager.get_boolean('canvas', 'setup_complete'):
			canvas_api_url = self.config_manager.get_configuration('canvas', 'url')
			canvas_api_key = self.config_manager.get_configuration('canvas', 'api_key')
			self.canvas_client = Canvas(canvas_api_url, canvas_api_key)
			self.course_map = self.create_course_map()
			self.update_terms_to_sync()

	def interactive_setup(self):
		printer.print_divider("Canvas Setup")
		canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
		self.config_manager.update_config('canvas', 'url', canvas_api_url)
		# canvas_api_key = input("Paste your Canvas API key: ")
		# self.config_manager.update_config('canvas', 'api_key', canvas_api_key)
		self.config_manager.update_config('canvas', 'setup_complete', 'True')
		self = CanvasManager(self.config_manager)
		self.select_terms_to_sync()

	def update_terms_to_sync(self):
		all_terms = self.get_terms()
		if self.config_manager.has_option('canvas', 'terms_to_skip') and self.config_manager.has_option('canvas', 'terms_to_sync'):
			skipped_terms = self.skipped_terms()
			selected_terms = self.selected_terms()
			for term in all_terms:
				if term not in skipped_terms and term not in selected_terms:
					selected_terms += [term]
			self.store_selected_terms(selected_terms)

	def skipped_terms(self):
		skipped_terms = ast.literal_eval(self.config_manager.get_configuration('canvas', 'terms_to_skip'))
		return skipped_terms

	def selected_terms(self):
		selected_terms = ast.literal_eval(self.config_manager.get_configuration('canvas', 'terms_to_sync'))
		return selected_terms

	def select_terms_to_sync(self):
		terms = self.get_terms()
		terminal_menu = TerminalMenu(terms, multi_select=True, show_multi_select_hint=True)
		print("Select the initial terms you would like to sync to Trello. Future terms will be added automatically.")
		menu_entry_indices = terminal_menu.show()
		selected_terms = list(terminal_menu.chosen_menu_entries)
		skipped = list(set(terms) - set(selected_terms))
		self.store_selected_terms(selected_terms)
		self.store_skipped_terms(skipped)

	def store_selected_terms(self, selected_terms):
		self.config_manager.update_config('canvas', 'terms_to_sync', str(selected_terms))

	def store_skipped_terms(self, skipped_terms):
		self.config_manager.update_config('canvas', 'terms_to_skip', str(skipped_terms))

	def create_course_map(self):
		user = self.canvas_client.get_current_user()
		courses = user.get_courses()
		course_map = defaultdict(list)
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
			term = self.get_course_term(name)
			# start_at = course.start_at

			# # A course number is required
			# if course_number:
			# 	course_map[course_number] = {"course" : course, "start_at" : start_at}

			# A term is required
			if term:
				course_map[term].append((course_number, course))
				# course_map[term] = {
				# 	course_number : {
				# 		"course" : course
				# 	}
				# }

		return course_map

	def get_terms(self):
		return list(self.course_map.keys())

	def get_course_number(self, name):
		# Returns the course number with the section number
		# Sample return = "CS_161_501" or "FES_365_501"
		course_number_pattern = re.compile(r"\w{2,3}_\d{3}_\d{3}")
		course_number = course_number_pattern.search(name)
		if course_number:
			course_number = course_number.group(0)
		else:
			course_number = False
		return course_number

	def get_course_term(self, name):
		# Returns the term of a course
		# Sample return = "W2021" for Winter 2021
		term_pattern = re.compile(r"\w{1}\d{4}")
		term = term_pattern.search(name)
		if term:
			term = term.group(0)
		else:
			term = False
		return term

	def get_course_year(self, course):
		start_at = course['start_at']
		if start_at is None:
			return None
		else:
			start_at = datetime.datetime.strptime(start_at, self.time_format)
		return start_at.year

	def in_current_year(self, course, current_year=datetime.date.today().year):
		course_year = self.get_course_year(course)
		return course_year == current_year

	def get_assignments(self, course):
		assignments = []
		all_assignments = course.get_assignments()
		for assignment in all_assignments:
			if not assignment.locked_for_user:
				assignments.append(assignment)
		return assignments

	def get_quizzes(self, course):
		quizzes = []
		all_quizzes = course.get_quizzes()
		for quiz in quizzes:
			if not quiz.locked_for_user:
				quizzes.append(quiz)
		return quizzes

	def get_assignment_name(self, assignment):
		if hasattr(assignment, "name"):
			assignment_name = assignment.name
		# Quizzes don't have names, they have titles
		else:
			assignment_name = assignment.title
		return assignment_name

	def get_submission_status(self, assignment):
		if hasattr(assignment, "has_submitted_submissions"):
			submitted = assignment.has_submitted_submissions
		# If assignment or quiz does not have the attribute, assume not submitted
		else:
			submitted = False
		return submitted
