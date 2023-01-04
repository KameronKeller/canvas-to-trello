import webbrowser
from commandline_printer import CommandLinePrinter as printer
from trello import TrelloClient

class TrelloManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager
		self.trello_client = TrelloClient(None)

	def interactive_setup(self):
		printer.print_divider("Trello Setup")
		input("Press enter to get your Trello API Key.")
		webbrowser.get().open("https://trello.com/app-key")
		trello_api_key = input("Paste the provided Trello API key here: ")
		trello_api_token = input("Generate a token and paste it here: ")
		self.config_manager.update_config('trello', 'api_key', trello_api_key)
		self.config_manager.update_config('trello', 'api_token', trello_api_token)
		self.trello_client = TrelloClient(
		    api_key=trello_api_key,
		    api_secret=trello_api_token
		)

