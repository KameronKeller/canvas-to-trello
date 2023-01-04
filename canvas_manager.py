from commandline_printer import CommandLinePrinter as printer

class CanvasManager:

	def __init__(self, config_manager):
		self.config_manager = config_manager

	def interactive_setup(self):
		printer.print_divider("Canvas Setup")
		canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
		self.config_manager.update_config('canvas', 'url', canvas_api_url)
		self.config_manager.update_config('canvas', 'api_key', "")
