import sqlite3
import datetime

class DatabaseManager:

	def __init__(self, canvas_manager, trello_manager, database_file='assignments.db'):
		self.canvas_manager = canvas_manager
		self.trello_manager = trello_manager
		self.database_file = database_file

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
					
		except sqlite3.Error as error:
			print("Error: ", error)
		finally:
			if connection:
				connection.close()
