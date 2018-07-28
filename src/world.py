import gc
import time
from misc import map_entity, flat_map
from requests import session
from tribalwars import Ally, Player, Village, Conquer


class World:
    # server, eg: pl121.plemiona.pl
    def __init__(self, server, refresh_interval):
        self.domain = server
        self.id2ally = {}
        self.id2player = {}
        self.id2village = {}
        self.conquers = []
        self.session = session()
        self.conquers = flat_map(self.__file('/map/conquer.txt'), Conquer)
        self.last_conquer_timestamp = self.conquers[-1].timestamp
        self.last_refresh = 0
        self.refresh_interval = refresh_interval
        self.refresh()

    def refresh(self):
        if self.last_refresh + self.refresh_interval * 60 < time.time():
            self.id2player = map_entity(self.__file('/map/player.txt'), Player)
            self.id2ally = map_entity(self.__file('/map/ally.txt'), Ally)
            self.id2village = map_entity(self.__file('/map/village.txt'), Village)
            self.last_refresh = time.time()
            gc.collect()

    def __file(self, path):
        url = 'https://{0}/{1}'.format(self.domain, path)
        response = self.session.get(url)
        print('fetching from {0} - [{1}]'.format(url, response.status_code))
        lines = [line for line in response.text.split('\n') if len(line) != 0]
        return lines

    def get_recent_conquers(self):
        conquers = flat_map(
            self.__file('/interface.php?func=get_conquer&since={}'.format(self.last_conquer_timestamp + 1)), Conquer)
        if len(conquers) > 0:
            self.last_conquer_timestamp = conquers[-1].timestamp
        return conquers

    def get_player_villages(self, player_id):
        return [village for village in self.id2village.values() if village.playerId == player_id]
