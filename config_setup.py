import configparser
import webbrowser
from simple_term_menu import TerminalMenu
from commandline_printer import CommandLinePrinter as printer

config = configparser.ConfigParser()

printer.print_divider("Canvas Setup")
canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
config['canvas'] = {'url': canvas_api_url,
					'api_key': ""}


printer.print_divider("Trello Setup")
input("Press enter to get your Trello API Key.")
webbrowser.get().open("https://trello.com/app-key")
trello_api_key = input("Paste the provided Trello API key here: ")
trello_api_token = input("Generate a token and paste it here: ")
config['trello'] = {'api_key': trello_api_key,
                    'api_token': trello_api_token}
