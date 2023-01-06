from config_manager import ConfigManager
import setup
import sync

def main():
	config_manager = ConfigManager()
	if config_manager.setup_complete():
		sync.sync()
	else:
		setup.setup()
		print("Syncing to Trello. This may take a few minutes...")
		sync.sync()

if __name__ == '__main__':
	main()
