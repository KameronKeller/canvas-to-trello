from config_manager import ConfigManager
import setup
import sync

def main():
	config_manager = ConfigManager()
	if config_manager.setup_complete():
		sync.sync()
	else:
		setup.setup()
		sync.sync()

if __name__ == '__main__':
	main()
