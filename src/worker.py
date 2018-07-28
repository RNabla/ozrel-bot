import time
from datetime import datetime
from misc import two_digit_number
from math import sqrt
from fbchat.models import *
from world import World


def workloop(fbclient, config):
    world = World(config['server'], 30)
    print('Server: ', config['server'], ' quiet: ', config['quiet'])
    while True:
        world.refresh()
        try:
            conquers = world.get_recent_conquers()
            for conquer in conquers:
                fb_ids = get_fb_ids(world, config['players'], conquer)
                if len(fb_ids) == 0:
                    continue
                plaintext = generate_plaintext(world, conquer)
                message = generate_message(plaintext, fb_ids, config['players'])
                if config['quiet'] == 'False':
                    fbclient.broadcast(message, config['thread_id'])
            time.sleep(int(config['sleep_time']) * 60)
        except Exception as e:
            print(e)


def get_fb_ids(world, players, conquer):
    fb_ids = []
    village = world.id2village.get(conquer.villageId)
    for fb_id in players:
        dist = int(players[fb_id]['range'])
        if any(distance(village, v) < dist for v in world.get_player_villages(players[fb_id]['tw_id'])):
            fb_ids.append(fb_id)
    return fb_ids


def generate_plaintext(world, conquer):
    village = world.id2village.get(conquer.villageId)
    winner = world.id2player.get(conquer.winnerPlayerId)
    loser = world.id2player.get(conquer.loserPlayerId)
    timestamp = datetime.fromtimestamp(conquer.timestamp)
    timepoint = u"{0}:{1}".format(
        two_digit_number(timestamp.hour),
        two_digit_number(timestamp.minute),
    )
    winner_tag = get_players_ally_tag(world, winner)
    if loser is None:
        msg = u"{0} {1} {2} podbija {3} (wioska barbarzyńska)".format(
            timepoint,
            winner.name,
            winner_tag,
            village.coords,
        )
    else:
        loser_tag = get_players_ally_tag(world, loser)
        msg = u"{0} {1} {2} podbija {3} od {4} {5}".format(
            timepoint,
            winner.name,
            winner_tag,
            village.coords,
            loser.name,
            loser_tag
        )
    return msg


def generate_message(plaintext, fb_ids, players):
    start = len(plaintext)
    mentions = []
    for fb_id in fb_ids:
        who = players[fb_id]['nick']
        plaintext = plaintext + u"@{0} ".format(who)
        mentions.append(Mention(fb_id, offset=start, length=len(who) + 1))
        start = start + len(who) + 2
    return Message(text=plaintext, mentions=mentions)


def get_players_ally_tag(world, player):
    if player.allyId == '0':
        return ""
    return "[{0}]".format(world.id2ally[player.allyId].tag)


def distance(village1, village2):
    part1 = village1.coords.split('|')
    part2 = village2.coords.split('|')
    dx = int(part1[0]) - int(part2[0])
    dy = int(part1[1]) - int(part2[1])
    return sqrt(dx * dx + dy * dy)
