import sqlite3
from commandline_printer import CommandLinePrinter as printer

class DatabaseManager:

	def __init__(self, canvas_manager, trello_manager, database_file='assignments.db', database_schema="database_schema.sql"):
		self.canvas_manager = canvas_manager
		self.trello_manager = trello_manager
		self.database_file = database_file
		self.database_schema = database_schema

	def setup_database(self):
		printer.print_divider("Database Setup")
		connection = sqlite3.connect(self.database_file)
		with open(self.database_schema, 'r') as sql_file:
			connection.executescript(sql_file.read())
		connection.close()

	def connect_to_database(self):
		connection = sqlite3.connect(self.database_file)
		cursor = connection.cursor()
		return connection, cursor

	def update_database(self):
		canvas_terms = self.canvas_manager.selected_terms()
		course_map = self.canvas_manager.course_map
		try:
			connection, cursor = self.connect_to_database()
			for term in canvas_terms:

				for course_name, course in course_map[term]:
					assignments = self.canvas_manager.get_assignments(course)
					quizzes = self.canvas_manager.get_quizzes(course)

					try:
						for assignment in assignments:
							self.add_to_database(connection, cursor, course_name, assignment)
					except Exception:
						print('No assignments found for: ', course_name)
						continue

					try:
						for quiz in quizzes:
							self.add_to_database(connection, cursor, course_name, quiz)
					except Exception:
						print('No quizzes found for: ', course_name)
						continue

			connection.close()
		except sqlite3.Error as error:
			print("SQLite Error in 'update_database': ", error)
		finally:
			if connection:
				connection.close()

	def add_to_database(self, connection, cursor, course_name, assignment):
		insert_query = """INSERT INTO ASSIGNMENTS
							VALUES (?, ?, ?, ?, ?, 0, '', 1, ?)
							ON CONFLICT(id) DO
								UPDATE SET
									assignment_name=?,
									due_date=?,
									submitted=?,
									sync_needed=1,
									assignment_link=?
								WHERE
									assignment_name <> ?
									OR
									due_date <> ?
									OR
									-- due_date is NULL
									-- OR
									submitted <> ?
									OR
									assignment_link <> ?"""

		selected_list = self.trello_manager.selected_list
		assignment_name = self.canvas_manager.get_assignment_name(assignment)
		submitted = self.canvas_manager.get_submission_status(assignment)
		assignment_id = assignment.id
		due_date = assignment.due_at
		assignment_link = self.canvas_manager.get_assignment_link(assignment)

		data = (assignment_id,
				course_name,
				assignment_name,
				due_date,
				submitted,
				assignment_link,
				assignment_name,
				due_date,
				submitted,
				assignment_link,
				assignment_name,
				due_date,
				submitted,
				assignment_link)

		cursor.execute(insert_query, data)
		connection.commit()

	def send_assignments_to_trello(self):
		search_query = """SELECT * FROM ASSIGNMENTS WHERE sync_needed = 1"""
		update_query = """UPDATE ASSIGNMENTS SET in_trello = 1, trello_card_id = ?, sync_needed = 0 WHERE id == ?"""
		labels_map = self.trello_manager.labels_map
		try:
			connection, cursor = self.connect_to_database()

			cursor.execute(search_query)
			data = cursor.fetchall()

			for row in data:
				assignment_id = int(row[0])
				course_name = row[1]
				assignment_name = row[2]
				due_date = row[3]
				submitted = row[4]
				in_trello = row[5]
				trello_card_id = row[6]
				sync_needed = row[7]
				assignment_link = row[8]

				labels = self.trello_manager.create_labels(submitted, course_name)

				if in_trello and sync_needed:
					card = self.trello_manager.update_card(trello_card_id, assignment_name, due_date, labels, self.canvas_manager.time_format, assignment_link)
					print('Δ updated: {}, {}'.format(course_name, assignment_name))
				elif sync_needed:
					card = self.trello_manager.add_card(assignment_name, due_date, labels, assignment_link)
					print('+ added: {}, {}'.format(course_name, assignment_name))

				update_data = (card.id, assignment_id)
				cursor.execute(update_query, update_data)
				connection.commit()

			connection.close()
		except sqlite3.Error as error:
			print("SQLite Error in 'send_assignments_to_trello':", error)
		finally:
			if connection:
				connection.close()
			print('Assignments successfully synced to Trello!')



