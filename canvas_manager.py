from commandline_printer import CommandLinePrinter as printer

class CanvasManager:

	def __init__(config_manager):
		self.config_manager = config_manager

	def interactive_setup():
		printer.print_divider("Canvas Setup")
		canvas_api_url = input("Paste your Canvas URL (e.g. https://canvas.oregonstate.edu/): ")
		config_manager.update_config('canvas', 'url', canvas_api_url)
		# config_manager['canvas'] = {'url': canvas_api_url,
		# 					'api_key': ""}
		# config_manager.write()
