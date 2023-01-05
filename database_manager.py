import sqlite3

class DatabaseManager:

	def __init__(self, canvas_manager, trello_manager, database_file='assignments.db'):
		self.canvas_manager = canvas_manager
		self.trello_manager = trello_manager
		self.database_file = database_file


