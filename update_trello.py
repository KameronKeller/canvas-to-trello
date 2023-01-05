from canvas_manager import CanvasManager
from config_manager import ConfigManager
from database_manager import DatabaseManager
from trello_manager import TrelloManager

config_manager = ConfigManager()
canvas_manager = CanvasManager(config_manager)
trello_manager = TrelloManager(config_manager)
database_manager = DatabaseManager(canvas_manager, trello_manager)

database_manager.update_database()

# database_manager.send_assignments_to_trello()
