import webbrowser
from commandline_printer import CommandLinePrinter as printer
from trello import TrelloClient
from simple_term_menu import TerminalMenu
import datetime

class TrelloManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager
		if self.config_manager.get_boolean('trello', 'setup_complete'):
			trello_api_key = self.config_manager.get_configuration('trello', 'api_key')
			trello_api_token = self.config_manager.get_configuration('trello', 'api_token')
			self.trello_client = TrelloClient(api_key=trello_api_key, api_secret=trello_api_token)
			self.selected_board = self.get_selected_board()
			self.selected_list = self.get_selected_list()
			self.labels_map = self.make_board_labels_map()

	def interactive_setup(self):
		printer.print_divider("Trello Setup")
		trello_api_key, trello_api_token = self.request_api_info()
		self.config_manager.update_config('trello', 'api_key', trello_api_key)
		self.config_manager.update_config('trello', 'api_token', trello_api_token)
		self.config_manager.update_config('trello', 'setup_complete', 'True')
		self.trello_client = TrelloClient(api_key=trello_api_key, api_secret=trello_api_token)
		selected_board = self.select_board()
		self.select_list(selected_board)

	def request_api_info(self):
		input("Press enter to get your Trello API Key.")
		webbrowser.get().open("https://trello.com/app-key")
		trello_api_key = input("Paste the provided Trello API key here: ")
		trello_api_token = input("Generate a token and paste it here: ")
		return trello_api_key, trello_api_token

	def get_board_names(self):
		boards = self.trello_client.list_boards('open')
		board_names = ['Create New']
		for board in boards:
			board_names.append(board.name)
		return board_names

	def select_board(self):
		board_names = self.get_board_names()
		terminal_menu = TerminalMenu(board_names)
		print("Select the Trello board you would like to copy Canvas assignments to.")
		menu_entry_index = terminal_menu.show()
		selected_board = board_names[menu_entry_index]
		if selected_board == 'Create New':
			selected_board = input("Type the name of the new board: ")
			self.trello_client.add_board(selected_board)
		selected_board = self.store_board_id(selected_board)
		return selected_board

	def store_board_id(self, name):
		board_map = self.create_board_map()
		selected_board = board_map[name]
		board_id = selected_board.id
		self.config_manager.update_config('trello', 'board_id', board_id)
		return selected_board

	def create_board_map(self, status='open'):
		all_boards = self.trello_client.list_boards('open')
		board_map = {board.name: board for board in all_boards}
		return board_map

	def select_list(self, board):
		list_names = self.get_list_names(board)
		terminal_menu = TerminalMenu(list_names)
		print("Select the board list you would like assignments to be added to.")
		menu_entry_index = terminal_menu.show()
		selected_list = list_names[menu_entry_index]
		if selected_list == 'Create New':
			selected_list = input("Type the name of the list: ")
			board.add_list(selected_list)
		self.store_list_id(board, selected_list)

	def get_list_names(self, board):
		board_lists = board.all_lists()
		list_names = ['Create New']
		for board_list in board_lists:
			list_names.append(board_list.name)
		return list_names

	def create_list_map(self, board):
		list_map = {list.name: list for list in board.list_lists()}
		return list_map

	def store_list_id(self, board, name):
		list_map = self.create_list_map(board)
		selected_list = list_map[name]
		self.config_manager.update_config('trello', 'list_id', selected_list.id)

	def get_selected_board(self):
		board_id = self.config_manager.get_configuration('trello', 'board_id')
		return self.trello_client.get_board(board_id)

	def get_board_label_names(self):
		labels = self.selected_board.get_labels()
		label_names = set()
		for label in labels:
			label_names.add(label.name)
		return label_names

	def make_board_labels_map(self):
		labels = self.selected_board.get_labels()
		labels_map = {}
		for label in labels:
			labels_map[label.name] = label
		if 'submitted' not in labels_map:
			submitted = self.add_label('Submitted', 'sky')
			labels_map['submitted'] = submitted
		return labels_map

	def add_label(self, name, color='yellow'):
		return self.selected_board.add_label(name, color)

	def get_selected_list(self):
		board = self.selected_board
		list_id = self.config_manager.get_configuration('trello', 'list_id')
		return board.get_list(list_id)

	def add_card(self, name, due_date, labels, assignment_link):
		return self.selected_list.add_card(name, desc=assignment_link, labels=labels, due=due_date)

	def update_card(self, id, name, due_date, labels, time_format, assignment_link):
		card = self.trello_client.get_card(id)
		existing_labels = set(card.labels)
		if due_date is not None:
			due_date = datetime.datetime.strptime(due_date, time_format)
			card.set_due(due_date)
		card.set_name(name)
		for label in labels:
			if label not in existing_labels:
				card.add_label(label)
		card_description = card.description
		if assignment_link not in card_description:
			card.set_description(card_description + '\n' + assignment_link)
		return card

	def create_labels(self, submitted, course_name):
		if course_name not in self.labels_map:
			label = self.add_label(course_name)
			self.labels_map[course_name] = label

		if submitted:
			labels = [self.labels_map[course_name], self.labels_map["submitted"]]
		else:
			labels = [self.labels_map[course_name]]

		return labels



