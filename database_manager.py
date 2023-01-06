import sqlite3
import datetime
from commandline_printer import CommandLinePrinter as printer

class DatabaseManager:

	def __init__(self, canvas_manager, trello_manager, database_file='assignments.db', database_schema="database_schema.sql"):
		self.canvas_manager = canvas_manager
		self.trello_manager = trello_manager
		self.database_file = database_file
		self.database_schema = database_schema
		self.insert_query = """INSERT INTO ASSIGNMENTS VALUES(?, ?, ?, ?, ?, ?, 0, '0') ON CONFLICT(id) DO UPDATE SET assignment_name=?, due_date=?, submitted=?, in_trello=0"""

	def setup_database(self):
		printer.print_divider("Database Setup")
		connection = sqlite3.connect(self.database_file)

		with open(self.database_schema, 'r') as sql_file:
			connection.executescript(sql_file.read())

		connection.close()

	def update_database(self):
		# current_year = datetime.date.today().year

		# for testing
		current_year = 2022

		course_map = self.canvas_manager.create_course_map()
		# label_names = self.trello_manager.get_board_label_names()
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
					
					# if course_name not in label_names:
					# 	self.trello_manager.add_label(course_name)
					# 	label_names.add(course_name)

					for assignment in assignments:
						self.add_to_database(connection, cursor, course_name, assignment, course['term'])

					for quiz in quizzes:
						self.add_to_database(connection, cursor, course_name, quiz, course['term'])

			connection.close()
		except sqlite3.Error as error:
			print("SQLite Error: ", error)
		finally:
			if connection:
				connection.close()


	def add_to_database(self, connection, cursor, course_name, assignment, term):
		selected_list = self.trello_manager.selected_list

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

	def send_assignments_to_trello(self):
		search_query = """SELECT * FROM ASSIGNMENTS WHERE in_trello = 0"""
		update_query = """UPDATE ASSIGNMENTS SET trello = 1, trello_card_id = ? WHERE id == ?"""

		labels_map = self.trello_manager.labels_map
		selected_list = self.trello_manager.selected_list

		try:
			connection = sqlite3.connect(self.database_file)
			cursor = connection.cursor()

			cursor.execute(search_query)
			data = cursor.fetchall()

			for row in data:
				assignment_id = int(row[0])
				course_name = row[1]
				assignment_name = row[2]
				due_date = row[3]
				submitted = row[5]
				in_trello = row[6]
				trello_card_id = row[7]

				if course_name not in labels_map:
					label = self.trello_manager.add_label(course_name)
					labels_map[course_name] = label


				if submitted:
					label_list = [labels_map[course_name], labels_map["submitted"]]
				else:
					label_list = [labels_map[course_name]]

				card = selected_list.add_card(assignment_name, desc=None, labels=label_list, due=due_date)
				update_data = (card.id, assignment_id)
				cursor.execute(update_query, update_data)
				connection.commit()

			connection.close()
		except sqlite3.Error as error:
			print("SQLite Error:", error)
		finally:
			if connection:
				connection.close()
			print('Assignments successfully copied to Trello!')



