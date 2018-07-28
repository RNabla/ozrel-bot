import getpass
from loader import get_configs
from ozrel import OzrelBot
from worker import workloop
from threading import Thread

email = input('Email: ')
password = getpass.getpass()

configs = get_configs()

client = OzrelBot(configs, email, password)
threads = [Thread(target=workloop, args=(client, configs[config])) for config in configs]
for thread in threads:
    thread.daemon = True
    thread.start()

client.listen()
