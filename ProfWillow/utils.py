#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import configargparse
import os
import sys
import json

log = logging.getLogger('utils')


def get_path(path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)
    return path


def get_args():
    if '-cf' not in sys.argv and '--config' not in sys.argv:
        config_files = [get_path('../config/config.ini')]
    parser = configargparse.ArgParser(default_config_files=config_files)
    parser.add_argument('-cf', '--config', is_config_file=True,
                        help='Configuration file')
    parser.add_argument('-token', '--tokens', type=str, action='append',
                        default=[], help='List of tokens for Discord bots',
                        required=True)
    parser.add_argument('-bcid', '--bot_client_ids', type=str,
                        action='append', default=[],
                        help='List of client ids for Discord Bots',
                        required=True)
    parser.add_argument('-feed', '--feed_channels', type=str,
                        action='append', default=[],
                        help='Channel ID that PokeAlarm posts to',
                        required=True)
    parser.add_argument('-sub', '--subscription_channel', type=str,
                        help=('Channel ID that users input subscription ' +
                              'commands'))
    parser.add_argument('-arc', '--active_raids_channel', type=str,
                        help='Channel ID to post active raids in',
                        required=True)
    parser.add_argument('-test', '--test_channel', type=str,
                        help='Channel ID that you would like to do testing in')
    parser.add_argument('-area', '--areas', type=str.lower, action='append',
                        default=[], help='List or areas or geofences')
    parser.add_argument('-muted', '--muted_role', type=str,
                        help='Role name for muted users')
    parser.add_argument('-aa', '--all_areas', action='store_true',
                        help=('default to sub to all areas when true ' +
                              'otherwise, default is no areas'), default=False)

    args = parser.parse_args()

    if len(args.tokens) != len(args.bot_client_ids):
        log.error("Token - Client ID mismatch")
        sys.exit(1)

    return args


class Dicts(object):
    users = []
    type_col = {'bug': 0xA8B820,
                'dark': 0x705848,
                'dragon': 0x7038F8,
                'electric': 0xF8D030,
                'fairy': 0xEE99AC,
                'fighting': 0xC03028,
                'fire': 0xF08030,
                'flying': 0xA890F0,
                'ghost': 0x705898,
                'grass': 0x78C850,
                'ground': 0xE0C068,
                'ice': 0x98D8D8,
                'normal': 0xA8A878,
                'poison': 0xA040A0,
                'psychic': 0xF85888,
                'rock': 0xB8A038,
                'steel': 0xB8B8D0,
                'water': 0x6890F0
                }
    pokemon = ['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon',
               'charizard', 'squirtle', 'wartortle', 'blastoise', 'caterpie',
               'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill',
               'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate',
               'spearow', 'fearow', 'ekans', 'arbok', 'pikachu', 'raichu',
               'sandshrew', 'sandslash', 'nidoran♀', 'nidorina', 'nidoqueen',
               'nidoran♂', 'nidorino', 'nidoking', 'clefairy', 'clefable',
               'vulpix', 'ninetales', 'jigglypuff', 'wigglytuff', 'zubat',
               'golbat', 'oddish', 'gloom', 'vileplume', 'paras', 'parasect',
               'venonat', 'venomoth', 'diglett', 'dugtrio', 'meowth',
               'persian', 'psyduck', 'golduck', 'mankey', 'primeape',
               'growlithe', 'arcanine', 'poliwag', 'poliwhirl', 'poliwrath',
               'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp',
               'bellsprout', 'weepinbell', 'victreebel', 'tentacool',
               'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta',
               'rapidash', 'slowpoke', 'slowbro', 'magnemite', 'magneton',
               "farfetch'd", 'doduo', 'dodrio', 'seel', 'dewgong', 'grimer',
               'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar',
               'onix', 'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb',
               'electrode', 'exeggcute', 'exeggutor', 'cubone', 'marowak',
               'hitmonlee', 'hitmonchan', 'lickitung', 'koffing', 'weezing',
               'rhyhorn', 'rhydon', 'chansey', 'tangela', 'kangaskhan',
               'horsea', 'seadra', 'goldeen', 'seaking', 'staryu', 'starmie',
               'mr. mime', 'scyther', 'jynx', 'electabuzz', 'magmar', 'pinsir',
               'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto', 'eevee',
               'vaporeon', 'jolteon', 'flareon', 'porygon', 'omanyte',
               'omastar', 'kabuto', 'kabutops', 'aerodactyl', 'snorlax',
               'articuno', 'zapdos', 'moltres', 'dratini', 'dragonair',
               'dragonite', 'mewtwo', 'mew', 'chikorita', 'bayleef',
               'meganium', 'cyndaquil', 'quilava', 'typhlosion', 'totodile',
               'croconaw', 'feraligatr', 'sentret', 'furret', 'hoothoot',
               'noctowl', 'ledyba', 'ledian', 'spinarak', 'ariados', 'crobat',
               'chinchou', 'lanturn', 'pichu', 'cleffa', 'igglybuff', 'togepi',
               'togetic', 'natu', 'xatu', 'mareep', 'flaaffy', 'ampharos',
               'bellossom', 'marill', 'azumarill', 'sudowoodo', 'politoed',
               'hoppip', 'skiploom', 'jumpluff', 'aipom', 'sunkern',
               'sunflora', 'yanma', 'wooper', 'quagsire', 'espeon', 'umbreon',
               'murkrow', 'slowking', 'misdreavus', 'unown', 'wobbuffet',
               'girafarig', 'pineco', 'forretress', 'dunsparce', 'gligar',
               'steelix', 'snubbull', 'granbull', 'qwilfish', 'scizor',
               'shuckle', 'heracross', 'sneasel', 'teddiursa', 'ursaring',
               'slugma', 'magcargo', 'swinub', 'piloswine', 'corsola',
               'remoraid', 'octillery', 'delibird', 'mantine', 'skarmory',
               'houndour', 'houndoom', 'kingdra', 'phanpy', 'donphan',
               'porygon2', 'stantler', 'smeargle', 'tyrogue', 'hitmontop',
               'smoochum', 'elekid', 'magby', 'miltank', 'blissey', 'raikou',
               'entei', 'suicune', 'larvitar', 'pupitar', 'tyranitar', 'lugia',
               'ho-oh', 'celebi']


def get_dicts(number_of_bots):
    dicts = Dicts()
    for bot_num in range(number_of_bots):
        dicts.users.append({})
    with open(get_path('../dicts/users.json')) as users_file:
        data = json.load(users_file)
        for user_id in data:
            dicts.users[int(user_id) % int(number_of_bots)][user_id] = data[
                user_id]
    return dicts


def update_dicts(number_of_bots):
    dicts = Dicts()
    master = {}
    for bot_num in range(number_of_bots):
        master.update(dicts.users[bot_num])
    with open(get_path('../dicts/users.json'), 'w') as users_file:
        json.dump(master, users_file, indent=4)


def truncate(msg):
    msg_split1 = msg[:len(msg[:1999].rsplit('\n', 1)[0])]
    msg_split2 = msg[len(msg[:1999].rsplit('\n', 1)[0]):]
    return [msg_split1, msg_split2]


def info_msg(feed_channels):
        info_msg = "Hello there! I am Professor Willow. \n"
        if feed_channels is True:
            info_msg += ("`%add eggs [level]` to get notifications when an " +
                         "given level egg appears at the top of a gym,\n" +
                         "`%add raids [level]` to get notifications when an " +
                         "give level of pokemon takes over a gym,\n" +
                         "`%add [pokemon]` to notifications when a given " +
                         "pokemon takes over a gym,\n" +
                         "`%delete eggs [level]` or `%remove eggs [level]` " +
                         "to delete notifications for below a given egg " +
                         "level,\n" +
                         "`%delete raids [level]` or `%remove raids " +
                         "[level]` to delete notifications for below a " +
                         "given raid level,\n" +
                         "`%delete [pokemon]` or `%remove [pokemon]` to " +
                         "delete notifications for a given raid pokemon,\n" +
                         "`%pause` or `%p` to pause all notifcations,\n" +
                         "`%pause [area/all]` to pause a given area or all " +
                         "areas,\n" +
                         "`%resume` or `%r` to resume all notifications,\n" +
                         "`%resume [area/all]` to resume a given area or " +
                         "all areas,\n" +
                         "`%subs` to see your notication settings,\n" +
                         "`%dex [pokemon]` to get pokemon information,\n" +
                         "`%status` to see which bots are currently " +
                         "online,\n" +
                         "`%donate` to see donation information for this " +
                         "project.\n" +
                         "It is possible to add or delete multiple pokemon " +
                         "by putting pokemon on seperate lines or " +
                         "separating them with commas.\n" +
                         "Commands should be in the " +
                         "raid_subscription_channel.\n\n" +
                         "To rsvp for a raid:\n" +
                         "Add the :arrow_right: reaction to a raid post to " +
                         "tell everyone you are on your way.\n" +
                         "Add the :white_check_mark: reaction to a raid " +
                         "post to tell everyone you have arrived at the " +
                         "raid.\n" +
                         "Add the :x: reaction to a raid post to tell " +
                         "everyone that you have either left a raid or are " +
                         "no longer on your way.")

        return info_msg
