# import configparser
import webbrowser
from simple_term_menu import TerminalMenu
from commandline_printer import CommandLinePrinter as printer
from config_manager import ConfigManager
from canvas_manager import CanvasManager

# config_parser = configparser.ConfigParser()

CONFIG_FILE = 'config.ini'
CONFIG_SECTIONS = ['canvas', 'trello', 'trello_board', 'trello_list']

config_manager = ConfigManager(CONFIG_FILE)

for section in CONFIG_SECTIONS:
	config_manager.add_config_section(section)

canvas_manager = CanvasManager(config_manager)

canvas_manager.interactive_setup()


# printer.print_divider("Trello Setup")
# input("Press enter to get your Trello API Key.")
# webbrowser.get().open("https://trello.com/app-key")
# trello_api_key = input("Paste the provided Trello API key here: ")
# trello_api_token = input("Generate a token and paste it here: ")
# config['trello'] = {'api_key': trello_api_key,
#                     'api_token': trello_api_token}

# with open('config.ini', 'w') as configfile:
#   config.write(configfile)

# trello_client = TrelloClient(
#     api_key=trello_api_key,
#     api_secret=trello_api_token
# )
