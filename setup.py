from config_manager import ConfigManager
from canvas_manager import CanvasManager
from trello_manager import TrelloManager
from database_manager import DatabaseManager

CONFIG_SECTIONS = ['canvas', 'trello']

config_manager = ConfigManager()

for section in CONFIG_SECTIONS:
	config_manager.add_config_section(section)
	config_manager.update_config(section, 'setup_complete', 'False')

canvas_manager = CanvasManager(config_manager)
trello_manager = TrelloManager(config_manager)
database_manager = DatabaseManager(canvas_manager, trello_manager)

canvas_manager.interactive_setup()
trello_manager.interactive_setup()
database_manager.setup_database()
