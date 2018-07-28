from urllib.parse import unquote_plus


class Ally:
    def __init__(self, line):
        parts = line.split(',')
        self.id = parts[0]
        self.name = unquote_plus(parts[1])
        self.tag = unquote_plus(parts[2])
        self.playersCount = parts[3]
        self.villagesCount = parts[4]
        self.top40Points = parts[5]
        self.points = parts[6]
        self.ranking = parts[7]


class Player:
    def __init__(self, line):
        parts = line.split(',')
        self.id = parts[0]
        self.name = unquote_plus(parts[1])
        self.allyId = parts[2]
        self.villagesCount = parts[3]
        self.points = parts[4]
        self.ranking = parts[5]


class Village:
    def __init__(self, line):
        parts = line.split(',')
        self.id = parts[0]
        self.name = unquote_plus(parts[1])
        self.x = parts[2]
        self.y = parts[3]
        self.coords = '{}|{}'.format(parts[2], parts[3])
        self.playerId = parts[4]
        self.points = parts[5]
        self.bonus = parts[6]


class Conquer:
    def __init__(self, line):
        parts = line.split(',')
        self.villageId = parts[0]
        self.timestamp = int(parts[1])
        self.winnerPlayerId = parts[2]
        self.loserPlayerId = parts[3]
