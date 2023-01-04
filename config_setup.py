# import configparser
# import webbrowser
from simple_term_menu import TerminalMenu
from commandline_printer import CommandLinePrinter as printer
from config_manager import ConfigManager
from canvas_manager import CanvasManager
from trello_manager import TrelloManager

# config_parser = configparser.ConfigParser()

CONFIG_FILE = 'config.ini'
CONFIG_SECTIONS = ['canvas', 'trello', 'trello_board', 'trello_list']

config_manager = ConfigManager(CONFIG_FILE)
canvas_manager = CanvasManager(config_manager)
trello_manager = TrelloManager(config_manager)

for section in CONFIG_SECTIONS:
	config_manager.add_config_section(section)

canvas_manager.interactive_setup()
trello_manager.interactive_setup()

# trello_client = TrelloClient(
#     api_key=trello_api_key,
#     api_secret=trello_api_token
# )
