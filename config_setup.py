from config_manager import ConfigManager
from canvas_manager import CanvasManager
from trello_manager import TrelloManager

CONFIG_FILE = 'config.ini'
CONFIG_SECTIONS = ['canvas', 'trello']

config_manager = ConfigManager(CONFIG_FILE)
canvas_manager = CanvasManager(config_manager)
trello_manager = TrelloManager(config_manager)

for section in CONFIG_SECTIONS:
	config_manager.add_config_section(section)

canvas_manager.interactive_setup()
trello_manager.interactive_setup()
