#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import asyncio
import discord
import requests
from bs4 import BeautifulSoup
from .utils import get_args, Dicts, update_dicts, truncate, info_msg

log = logging.getLogger('commands')

args = get_args()
dicts = Dicts()


async def status(client, message, bot_number):
    await asyncio.sleep(bot_number * 0.1)
    delete = await client.send_message(
        message.channel, 'Professor Willow ({} of {}) standing by.'.format(
            bot_number, len(args.tokens)))
    if bot_number == 1:
        await asyncio.sleep(0.1 * int(len(args.tokens)))
        delete_vid = await client.send_message(
            message.channel, 'https://youtu.be/kxH6YErAIgA')
        await asyncio.sleep(60 - (0.1 * (int(len(args.tokens)) + 1)))
        await client.delete_message(delete_vid)
        await client.delete_message(delete)
        await client.delete_message(message)
    else:
        await asyncio.sleep(60 - (0.1 * bot_number))
        await client.delete_message(delete)


async def add_eggs(client, message, bot_number):
    try:
        msg = message.content.lower().split()[2]
        if int(msg) <= 5:
            if message.author.id not in dicts.users[bot_number]:
                dicts.users[bot_number][message.author.id] = {'pokemon': [],
                                                              'raids': None,
                                                              'eggs': int(msg),
                                                              'paused': False}
                if args.all_areas is True:
                    dicts.users[bot_number][message.author.id][
                        'areas'] = args.areas
                else:
                    dicts.users[bot_number][message.author.id]['areas'] = []
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`, I will alert you if any `Level {}+ eggs` ' +
                    'appear at the top of a gym.').format(
                        message.author.display_name, msg))
            elif (dicts.users[bot_number][message.author.id][
                'eggs'] is not None and dicts.users[bot_number][
                    message.author.id]['eggs'] <= int(msg)):
                await client.send_message(message.channel, (
                    '`{}`, I am  already alerting you if any ' +
                    '`Level {}+ eggs` appear at the top of a gym.').format(
                        message.author.display_name, msg))
            else:
                dicts.users[bot_number][message.author.id]['eggs'] = int(msg)
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`, I will alert you if any `Level {}+ egg` ' +
                    'appear at the top of any gyms.').format(
                        message.author.display_name, msg))
        else:
            await client.send_message(message.channel, (
                'Egg level must be less than or equal to `5`, try again ' +
                '`{}`.').format(message.author.display_name))
    except:
        await client.send_message(message.channel, (
            'Egg level must be an integer, try again `{}`.').format(
                message.author.display_name))


async def add_raids(client, message, bot_number):
    try:
        msg = message.content.lower().split()[2]
        if int(msg) <= 5:
            if message.author.id not in dicts.users[bot_number]:
                dicts.users[bot_number][message.author.id] = {
                    'pokemon': [],
                    'raids': int(msg),
                    'eggs': None,
                    'paused': False}
                if args.all_areas is True:
                    dicts.users[bot_number][message.author.id][
                        'areas'] = args.areas
                else:
                    dicts.users[bot_number][message.author.id]['areas'] = []
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`. I will alert you if any `Level {}+ pokemon` ' +
                    'take over a gym.').format(
                        message.author.display_name, msg))
            elif dicts.users[bot_number][message.author.id][
                'raids'] is not None and dicts.users[bot_number][
                    message.author.id]['raids'] <= int(msg):
                await client.send_message(message.channel, (
                    '`{}`, I am  already alerting you if any ' +
                    '`Level {}+ pokemon` take over a gym.').format(
                        message.author.display_name, msg))
            else:
                dicts.users[bot_number][message.author.id]['raids'] = int(msg)
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`. I will alert you if any `Level {}+ pokemon` ' +
                    'take over a gym.').format(
                        message.author.display_name, msg))
        else:
            await client.send_message(message.channel, (
                'Raid level must be less than or equal to `5`, try again ' +
                '`{}`.').format(message.author.display_name))
    except:
        await client.send_message(message.channel, (
            'Raid level must be an integer, try again `{}`.').format(
                message.author.display_name))


async def add(client, message, bot_number):
    msg = message.content.lower().replace('%add ', '').replace(
        '%add\n', '').replace('nidoran♀', 'nidoranf').replace(
        'nidoran♂', 'nidoranm').replace(',\n', ',').replace('\n', ',').replace(
        ', ', ',').split(',')
    for cmd in msg:
        if cmd in dicts.pokemon:
            if message.author.id not in dicts.users[bot_number]:
                dicts.users[bot_number][message.author.id] = {
                    'pokemon': [cmd],
                    'raids': None,
                    'eggs': None,
                    'paused': False}
                if args.all_areas is True:
                    dicts.users[bot_number][message.author.id][
                        'areas'] = args.areas
                else:
                    dicts.users[bot_number][message.author.id]['areas'] = []
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`. I will alert you if a(n) `{}` takes over a ' +
                    'gym.').format(message.author.display_name, cmd.title()))
            elif cmd in dicts.users[bot_number][message.author.id]['pokemon']:
                await client.send_message(message.channel, (
                    '`{}`, I am  already alerting you if a(n) ' +
                    '`{}` takes over a gym.').format(
                        message.author.display_name, cmd.title()))
            else:
                dicts.users[bot_number][message.author.id]['pokemon'].append(
                    cmd)
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`. I will alert you if a(n) `{}` takes over a ' +
                    'gym.').format(message.author.display_name, cmd.title()))
        else:
            await client.send_message(message.channel, (
                "That's not any pokemon that I know of, check your spelling " +
                "and try again `{}`.").format(message.author.display_name))


async def delete_eggs(client, message, bot_number):
    try:
        msg = message.content.lower().split()[2]
        if int(msg) <= 5:
            if (message.author.id not in dicts.users[bot_number] or
                dicts.users[bot_number][message.author.id]['eggs'] is None or
                    dicts.users[bot_number][message.author.id]['eggs'] > int(
                        msg)):
                await client.send_message(message.channel, (
                    "`{}`, I wasn't previously alerting you if any " +
                    "`Level {} eggs` appear at the top of a gym.").format(
                        message.author.display_name, msg))
            else:
                dicts.users[bot_number][message.author.id][
                    'eggs'] = int(msg) + 1
                if dicts.users[bot_number][message.author.id]['eggs'] == 6:
                    dicts.users[bot_number][message.author.id]['eggs'] = None
                if (dicts.users[bot_number][message.author.id][
                    'pokemon'] == [] and dicts.users[bot_number][
                        message.author.id]['raids'] is None and
                    dicts.users[bot_number][message.author.id][
                        'eggs'] is None):
                    dicts.users[bot_number].pop(message.author.id)
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`, I will no longer alert you if any ' +
                    '`Level {} or below eggs` appear at the top of a ' +
                    'gym.').format(message.author.display_name, msg))
        else:
            await client.send_message(message.channel, (
                'Egg level must be less than or equal to `5`, try again ' +
                '`{}`.').format(message.author.display_name))
    except:
        await client.send_message(message.channel, (
            'Egg level must be an integer, try again `{}`.').format(
                message.author.display_name))


async def delete_raids(client, message, bot_number):
    try:
        msg = message.content.lower().split()[2]
        if int(msg) <= 5:
            if (message.author.id not in dicts.users[bot_number] or
                dicts.users[bot_number][message.author.id]['raids'] is None or
                    dicts.users[bot_number][message.author.id]['raids'] > int(
                        msg)):
                await client.send_message(message.channel, (
                    "`{}`, I wasn't previously alerting you if any " +
                    "`Level {} pokemon` take over a gym.").format(
                        message.author.display_name, msg))
            else:
                dicts.users[bot_number][message.author.id][
                    'raids'] = int(msg) + 1
                if dicts.users[bot_number][message.author.id]['raids'] == 6:
                    dicts.users[bot_number][message.author.id]['raids'] = None
                if (dicts.users[bot_number][message.author.id][
                    'pokemon'] == [] and dicts.users[bot_number][
                        message.author.id]['raids'] is None and
                    dicts.users[bot_number][message.author.id][
                        'eggs'] is None):
                    dicts.users[bot_number].pop(message.author.id)
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`, I will no longer alert you if any ' +
                    '`Level {} or below pokemon` take over a gym').format(
                        message.author.display_name, msg))
        else:
            await client.send_message(message.channel, (
                'Egg level must be less than or equal to `5`, try again ' +
                '`{}`.').format(message.author.display_name))
    except:
        await client.send_message(message.channel, (
            'Egg level must be an integer, try again `{}`.').format(
                message.author.display_name))


async def delete(client, message, bot_number):
    msg = message.content.lower().replace('%delete ', '').replace(
        '%delete\n', '').replace('%remove ', '').replace(
        '%remove\n', '').replace('%gtfo ', '').replace('%gtfo\n', '').replace(
        'nidoran♀', 'nidoranf').replace('nidoran♂', 'nidoranm').replace(
        ',\n', ',').replace('\n', ',').replace(', ', ',').split(',')
    for cmd in msg:
        if cmd in dicts.pokemon:
            if (message.author.id not in dicts.users[bot_number] or
                cmd not in dicts.users[bot_number][message.author.id][
                    'pokemon']):
                await client.send_message(message.channel, (
                    "`{}`, I wasn't previously alerting you if a(n) `{}` " +
                    "takes over a gym.").format(
                        message.author.display_name, cmd.title()))
            else:
                dicts.users[bot_number][message.author.id][
                    'pokemon'].remove(cmd)
                if (dicts.users[bot_number][message.author.id][
                    'pokemon'] == [] and dicts.users[bot_number][
                        message.author.id]['raids'] is None and
                    dicts.users[bot_number][message.author.id][
                        'eggs'] is None):
                    dicts.users[bot_number].pop(message.author.id)
                update_dicts(len(args.tokens))
                await client.send_message(message.channel, (
                    'Okay `{}`, I will no longer alert you if a(n) ' +
                    '`{}` takes over a gym').format(
                        message.author.display_name, cmd.title()))
        else:
            await client.send_message(message.channel, (
                "That's not any pokemon that I know of, check your spelling " +
                "and try again `{}`.").format(message.author.display_name))


async def pause(client, message, bot_number):
    if message.author.id not in dicts.users[bot_number]:
        await client.send_message(message.channel, (
            "There is nothing to pause, `{}`, I'm not alerting you to any " +
            "raids or eggs.").format(message.author.display_name))
    elif dicts.users[bot_number][message.author.id]['paused'] is True:
        await client.send_message(message.channel, (
            'Your alerts are already paused, `{}`.').format(
                message.author.display_name))
    else:
        dicts.users[bot_number][message.author.id]['paused'] = True
        update_dicts(len(args.tokens))
        await client.send_message(message.channel, (
            'Your alerts have been paused, `{}`.').format(
                message.author.display_name))


async def pause_area(client, message, bot_number):
    if message.content.lower() == '%pause all':
        areas = args.areas
    else:
        areas = message.content.lower().replace('%pause ', '').replace(
                '%pause\n', '').replace(',\n', ',').replace('\n', ',').replace(
                ', ', ',').split(',')
    msg = ""
    for area in areas:
        if area in args.areas:
            if message.author.id not in dicts.users[bot_number]:
                msg = (msg + (
                    "There is nothing to pause, `{}`, I'm not alerting you " +
                    "to any raids or eggs.\n").format(
                        message.author.display_name))
            elif area not in dicts.users[bot_number][message.author.id][
                    'areas']:
                msg = (msg + (
                    'Your alerts are already paused for the `{}` area, ' +
                    '`{}`.\n').format(
                        area.title(), message.author.display_name))
            else:
                dicts.users[bot_number][
                    message.author.id]['areas'].remove(area)
                update_dicts(len(args.tokens))
                msg = (msg + (
                    'Your alerts have been paused for the `{}` area, ' +
                    '`{}`.\n').format(
                        area.title(), message.author.display_name))
        else:
            msg = (msg + (
                "That's not any area I know of in this region, `{}`\n").format(
                    message.author.display_name))
    if len(msg) > 0:
        await sendBigText(client, msg, find_user(message.author.id, client))
    await client.delete_message(message)


async def resume(client, message, bot_number):
    if message.author.id not in dicts.users[bot_number]:
        await client.send_message(message.channel, (
            "There is nothing to resume, `{}`, I'm not alerting you to any " +
            "raids or eggs.").format(message.author.display_name))
    elif dicts.users[bot_number][message.author.id]['paused'] is False:
        await client.send_message(message.channel, (
            'Your alerts were not previously paused, `{}`.').format(
                message.author.display_name))
    else:
        dicts.users[bot_number][message.author.id]['paused'] = False
        update_dicts(len(args.tokens))
        await client.send_message(message.channel, (
            'You alerts have been resumed, `{}`.').format(
                message.author.display_name))


async def resume_area(client, message, bot_number):
    if message.content.lower() == '%resume all':
        areas = args.areas
    else:
        areas = message.content.lower().replace('%resume ', '').replace(
                '%resume\n', '').replace(',\n', ',').replace(
                '\n', ',').replace(', ', ',').split(',')
    msg = ""
    for area in areas:
        if area in args.areas:
            if message.author.id not in dicts.users[bot_number]:
                msg = (msg + ("There is nothing to resume, I'm not " +
                       "alerting you to any raids or eggs.\n"))
            elif area in dicts.users[bot_number][message.author.id]['areas']:
                msg = (msg + ('Your alerts were not previously paused for ' +
                       'the `{}` area.\n').format(area.title()))
            else:
                dicts.users[bot_number][
                    message.author.id]['areas'].append(area)
                update_dicts(len(args.tokens))
                msg = (msg + ('Your alerts have been resumed for the `{}` ' +
                       'area.\n').format(area.title()))
        else:
            msg = (msg + ("That's not any area I know of in this region\n"
                          ).format(message.author.display_name))
    if len(msg) > 0:
        await sendBigText(client, msg, find_user(message.author.id, client))
    await client.delete_message(message)


async def sendBigText(client, message, destination):
    if len(message) < 2000:
        await client.send_message(destination, message)
    else:
        lines = message.split("\n")
        msg = ""
        for line in lines:
            if len(line) + len(msg) + 1 > 2000:
                await client.send_message(destination, msg)
                msg = ""
            else:
                msg = msg + "\n" + line
        if len(msg) > 0:
            await client.send_message(destination, msg)


async def subs(client, message, bot_number):
    msg = message.author.display_name + "'s Raid Notification Settings:\n"
    if message.author.id in dicts.users[bot_number]:
        if dicts.users[bot_number][message.author.id]['paused'] is True:
            msg += '\nPAUSE MODE: ON\n'
        else:
            msg += '\nPAUSE MODE: OFF\n'
        if args.all_areas is True:
            msg += '\n__PAUSED AREAS__\n'
            if len(args.areas) == len(dicts.users[bot_number][
                message.author.id][
                    'areas']):
                msg += 'None\n'
            else:
                for area in list(set(args.areas) - set(dicts.users[bot_number][
                        message.author.id]['areas'])):
                    msg += area.title() + '\n'
        else:
            msg += '\n__ALERT AREA__\n'
            for area in dicts.users[bot_number][message.author.id]['areas']:
                msg += area.title() + '\n'
        msg += '\nEGG ALERT LEVEL: ' + str(dicts.users[bot_number][
            message.author.id]['eggs']) + '+'
        msg += '\nRAID ALERT LEVEL: ' + str(dicts.users[bot_number][
            message.author.id]['raids']) + '+\n'
        msg += '\n__RAID ALERTS__\n'
        if dicts.users[bot_number][message.author.id]['pokemon'] == []:
            msg += 'None'
        else:
            for pokemon in dicts.users[bot_number][message.author.id][
                    'pokemon']:
                msg += pokemon + '\n'
        msg = [msg]
        while len(msg[-1]) > 2000:
            for msg_split in truncate(msg.pop()):
                msg.append(msg_split)
        for dm in msg:
            await client.send_message(discord.utils.find(
                lambda u: u.id == message.author.id, client.get_all_members()),
                                      dm)
    else:
        await client.send_message(find_user(message.author.id, client),
                                  "You haven't set any subscriptions!")
    await client.delete_message(message)


def dex(client, message):
    pokemon = message.content.lower().split()[1]
    if pokemon in dicts.pokemon:
        dex_number = dicts.pokemon.index(pokemon) + 1

        site = "https://pokemongo.gamepress.gg/pokemon/{}".format(dex_number)
        page = requests.get(site)
        soup = BeautifulSoup(page.content, 'html.parser')

        rating = soup.find_all(class_="pokemon-rating")
        max_cp = soup.find_all(class_="max-cp-number")
        stats = soup.find_all(class_="stat-text")
        types = soup.find_all(class_=("field field--name-field-pokemon-type " +
                                      "field--type-entity-reference " +
                                      "field--label-hidden field__items"))
        female = soup.find_all(class_="female-percentage")
        male = soup.find_all(class_="male-percentage")

        quick = []
        legacy_quick = []
        for quick_move in soup.find_all(class_=(
                "views-field views-field-field-quick-move")):
            quick.append(quick_move.find(class_=(
                "field field--name-title " +
                "field--type-string field--label-hidden")))
            legacy_quick.append(quick_move.find(class_=(
                "move-info")))

        charge = []
        legacy_charge = []
        for charge_move in soup.find_all(class_=(
                "views-field views-field-field-charge-move")):
            charge.append(charge_move.find(class_=(
                "field field--name-title " +
                "field--type-string field--label-hidden")))
            legacy_charge.append(charge_move.find(class_=(
                "move-info")))

        legacy_moves = []
        for (legacy_quick, legacy_charge) in zip(legacy_quick, legacy_charge):
            try:
                if legacy_quick.get_text() == '* ':
                    legacy_moves.append(' (Legacy)')
                else:
                    try:
                        if legacy_charge.get_text() == '* ':
                            legacy_moves.append(' (Legacy)')
                        else:
                            legacy_moves.append('')
                    except:
                        legacy_moves.append('')
            except:
                try:
                    if legacy_charge.get_text() == '* ':
                        legacy_moves.append(' (Legacy)')
                    else:
                        legacy_moves.append('')
                except:
                    legacy_moves.append('')

        offensive_grade = soup.find_all(class_=(
            "views-field views-field-field-offensive-moveset-grade"))
        for index, grade in enumerate(offensive_grade):
            offensive_grade[index] = str(grade.get_text().strip())
        defensive_grade = soup.find_all(class_=(
            "views-field views-field-field-defensive-moveset-grade"))
        for index, grade in enumerate(defensive_grade):
            defensive_grade[index] = str(grade.get_text().strip())

        offensive_moves = sorted(zip(offensive_grade[1:], quick[1:],
                                     charge[1:], legacy_moves[1:]),
                                 key=lambda x: x[0])
        defensive_moves = sorted(zip(defensive_grade[1:], quick[1:],
                                     charge[1:], legacy_moves[1:]),
                                 key=lambda x: x[0])

        if len(soup.find_all(class_=("raid-boss-counters"))) > 0:
            raid_counters = soup.find_all(class_=("raid-boss-counters"))[
                0].find_all(class_=("field field--name-title " +
                                    "field--type-string field--label-hidden"))

        title = "%03d" % dex_number + ' | ' + pokemon.upper()
        try:
            descript = "Rating: " + rating[0].get_text().strip() + ' / 10'
        except:
            descript = "Rating: - / 10"
        if len(types[0].get_text().split()) == 1:
            descript += "\nType: " + types[0].get_text().split()[0]
        else:
            descript += ("\nType: " + types[0].get_text().split()[0] + ' | ' +
                         types[0].get_text().split()[1])
        descript += "\nMax CP: " + max_cp[0].get_text()
        descript += ("\n" + stats[0].get_text().split()[0] + ' ' +
                     stats[0].get_text().split()[1] + ' | ' +
                     stats[1].get_text().split()[0] + ' ' +
                     stats[1].get_text().split()[1] + ' | ' +
                     stats[2].get_text().split()[0] +
                     ' ' + stats[2].get_text().split()[1] + '\n')
        try:
            descript += ("Female: " + female[0].get_text().strip() +
                         " | Male: " + male[0].get_text().strip() + '\n')
        except:
            pass

        if len(offensive_moves) > 0:

            descript += "\nAttacking Movesets:\n```"
            for (grade, quick, charge, legacy) in offensive_moves:
                descript += ('\n[' + grade.strip() + '] ' + quick.get_text() +
                             ' / ' + charge.get_text() + legacy)
            descript += " \n```"

            descript += "\nDefensive Movesets:\n```"
            for (grade, quick, charge, legacy) in defensive_moves:
                descript += ('\n[' + grade.strip() + '] ' + quick.get_text() +
                             ' / ' + charge.get_text() + legacy)
            descript += "\n```"

            if len(soup.find_all(class_=("raid-boss-counters"))) > 0:

                descript += "\nRaid Boss Counters:\n```"
                for counter in raid_counters:

                    descript += '\n' + counter.get_text()
                descript += "\n```"

        else:

            quick_moves = soup.find(class_=("primary-move")).find_all(class_=(
                "field field--name-title field--type-string " +
                "field--label-hidden"))
            charge_moves = soup.find(class_=("secondary-move")).find_all(
                class_=("field field--name-title field--type-string " +
                        "field--label-hidden"))
            if soup.find(class_=("pokemon-legacy-quick-moves")) is not None:
                quick_legacy = soup.find(class_=(
                    "pokemon-legacy-quick-moves")).find_all(class_=(
                        "field field--name-title field--type-string " +
                        "field--label-hidden"))
            if soup.find(class_=(
                    "secondary-move-legacy secondary-move")) is not None:
                charge_legacy = soup.find(class_=(
                    "secondary-move-legacy secondary-move")).find_all(class_=(
                        "field field--name-title field--type-string " +
                        "field--label-hidden"))

            descript += "\nQuick Moves:\n```"
            for quick_move in quick_moves:
                descript += '\n' + quick_move.get_text()
            if soup.find(class_=("pokemon-legacy-quick-moves")) is not None:
                for legacy_move in quick_legacy:
                    descript += '\n' + legacy_move.get_text() + ' (Legacy)'
            descript += "\n```"

            descript += "\nCharge Moves:\n```"
            for charge_move in charge_moves:
                descript += '\n' + charge_move.get_text()
            if soup.find(class_=(
                    "secondary-move-legacy secondary-move")) is not None:
                for legacy_move in charge_legacy:
                    descript += '\n' + legacy_move.get_text() + ' (Legacy)'
            descript += "\n```"

            if len(soup.find_all(class_=("raid-boss-counters"))) > 0:

                descript += "\nRaid Boss Counters:\n```"
                for counter in raid_counters:

                    descript += '\n' + counter.get_text()
                descript += "\n```"

        em = discord.Embed(title=title, url=site, description=descript,
                           color=dicts.type_col[
                               types[0].get_text().split()[0].lower()])
        em.set_thumbnail(
            url=('https://raw.githubusercontent.com/Gladiator10864/PokeAlarm/' +
                 'master/icons/{}.png').format(dex_number))
        return client.send_message(message.channel, embed=em)
    else:
        return client.send_message(message.channel, (
            "That's not any pokemon I know of, check your spelling " +
            "`{}`").format(message.author.display_name))


async def commands(client, message):
    delete = await client.send_message(
        message.channel, info_msg(args.feed_channels != []))
    await client.delete_message(message)
    await asyncio.sleep(60)
    await client.delete_message(delete)


async def areas(client, message):
    msg = ("Valid areas: \n" +
           "\n".join(sorted(args.areas)).title())
    delete = await client.send_message(
        message.channel, msg)
    await client.delete_message(message)
    await asyncio.sleep(60)
    await client.delete_message(delete)


async def donate(client, message):
    msg_title = "DONATION INFORMATION"
    descript = ("Support this project!\n" +
                "PayPal: https://www.paypal.me/dneal12\n" +
                "Patreon - https://www.patreon.com/dneal12\n" +
                "Please note: this donation goes directly into the \n"
                "pocket of the bot dev, not this Discord server.")
    col = int('0x85bb65', 16)
    em = discord.Embed(title=msg_title, description=descript, color=col)
    await client.send_message(message.channel, embed=em)
    await client.delete_message(message)


def find_user(id, client):
    return discord.utils.find(lambda u: u.id == id, client.get_all_members())
