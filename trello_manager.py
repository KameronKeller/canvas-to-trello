import webbrowser
from commandline_printer import CommandLinePrinter as printer
from trello import TrelloClient
from simple_term_menu import TerminalMenu

class TrelloManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager
		self.trello_client = TrelloClient(None)

	def interactive_setup(self):
		printer.print_divider("Trello Setup")
		trello_api_key, trello_api_token = self.request_api_info()
		# input("Press enter to get your Trello API Key.")
		# webbrowser.get().open("https://trello.com/app-key")
		# trello_api_key = input("Paste the provided Trello API key here: ")
		# trello_api_token = input("Generate a token and paste it here: ")
		self.config_manager.update_config('trello', 'api_key', trello_api_key)
		self.config_manager.update_config('trello', 'api_token', trello_api_token)
		self.trello_client = TrelloClient(api_key=trello_api_key, api_secret=trello_api_token)
		board_names = self.get_board_list()
		selected_board = self.select_board(board_names)

	def request_api_info(self):
		input("Press enter to get your Trello API Key.")
		webbrowser.get().open("https://trello.com/app-key")
		trello_api_key = input("Paste the provided Trello API key here: ")
		trello_api_token = input("Generate a token and paste it here: ")
		return trello_api_key, trello_api_token

	def get_board_list(self):
		boards = self.trello_client.list_boards('open')
		board_names = ['Create New']
		for board in boards:
			board_names.append(board.name)
		return board_names

	def select_board(self, board_names):
		terminal_menu = TerminalMenu(board_names)
		print("Select the Trello board you would like to copy Canvas assignments to.")
		menu_entry_index = terminal_menu.show()
		return board_names[menu_entry_index]

