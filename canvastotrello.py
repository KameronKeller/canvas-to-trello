from config_manager import ConfigManager

def main():
	config_manager = ConfigManager()
	if config_manager.setup_complete():
		sync_trello()
	else:
		setup()

if __name__ == '__main__':
	main()
