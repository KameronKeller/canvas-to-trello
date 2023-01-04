import configparser
from simple_term_menu import TerminalMenu
from commandline_printer import CommandLinePrinter as printer

config = configparser.ConfigParser()

printer.print_divider("Canvas Setup")
canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
config['canvas'] = {'url': canvas_api_url,
					'api_key': ""}

