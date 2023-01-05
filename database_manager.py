import sqlite3
import datetime

class DatabaseManager:

	def __init__(self, canvas_manager, trello_manager, database_file='assignments.db'):
		self.canvas_manager = canvas_manager
		self.trello_manager = trello_manager
		self.database_file = database_file
		self.insert_query = """INSERT INTO ASSIGNMENTS VALUES(?, ?, ?, ?, ?, ?, 0) ON CONFLICT(id) DO UPDATE SET assignment_name=?, due_date=?, submitted=?, trello=0"""

	def update_database(self):
		# current_year = datetime.date.today().year
		# for testing
		current_year = 2022

		course_map = self.canvas_manager.create_course_map()
		try:
			connection = sqlite3.connect(self.database_file)
			cursor = connection.cursor()
			for course_name, course in course_map.items():
				start_at = course['start_at']
				if start_at is not None:
					start_at = datetime.datetime.strptime(start_at, self.canvas_manager.time_format)
				if start_at is not None and start_at.year == current_year:
					assignments = course['course'].get_assignments()
					quizzes = course['course'].get_quizzes()
					label_names = self.trello_manager.get_board_label_names()
					
					if course_name not in label_names:
						self.trello_manager.add_label(course_name)

					for assignment in assignments:
						self.add_to_database(course_name, assignment, course['term'])

					for quiz in quizzes:
						self.add_to_database(course_name, quiz, course['term'])

		except sqlite3.Error as error:
			print("Error: ", error)
		finally:
			if connection:
				connection.close()

	def add_to_database(self, course_name, assignment, term):
		selected_list = self.trello_manager.get_selected_list()
		try:
			connection = sqlite3.connect(self.database_file)
			cursor = connection.cursor()	

			if hasattr(assignment, "name"):
				assignment_name = assignment.name
			# Quizzes don't have names, they have titles
			else:
				assignment_name = assignment.title

			if hasattr(assignment, "has_submitted_submissions"):
				submitted = assignment.has_submitted_submissions
			else:
				submitted = False

			assignment_id = assignment.id
			due_date = assignment.due_at
			data = (assignment_id, course_name, assignment_name, due_date, term, submitted, assignment_name, due_date, submitted)
			cursor.execute(self.insert_query, data)
			connection.commit()
		except sqlite3.Error as error:
			print("Error:", error)
		finally:
			if connection:
				connection.close()

