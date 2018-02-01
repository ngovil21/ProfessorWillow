#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import discord
import asyncio
import re
from .utils import get_args, Dicts

log = logging.getLogger('notification')

args = get_args()
dicts = Dicts()


async def send_msgs(client, bot_number):
    while True:
        await asyncio.sleep(0.1)
        for obj in dicts.msgs[bot_number]:
            if type(obj) == list:
                try:
                    msg = await client.send_message(discord.utils.find(
                        lambda u: u.id == obj[0], client.get_all_members()),
                                                   embed=obj[1])
                    log.info("Sending raid to {}".format(
                        msg.channel.recipients[0].display_name))
                except:
                    log.error(('Faild to send: To {} probably due to the ' +
                               'end-user blocking the bot').format(
                          discord.utils.find(
                              lambda u: u.id == obj[0],
                              client.get_all_members()).display_name))
                    continue
            elif isinstance(obj, discord.message.Message):
                msg = obj
                log.info("Reacting to msg in {}".format(msg.channel.name))
            await client.add_reaction(msg, '➡')
            await asyncio.sleep(0.25)
            await client.add_reaction(msg, '✅')
            await asyncio.sleep(0.25)
            await client.add_reaction(msg, '❌')
            await asyncio.sleep(0.25)
            dicts.msgs[bot_number].remove(obj)
            log.info("Queue size for bot number {}: {}".format(
                bot_number + 1, len(dicts.msgs[bot_number])))
            if len(dicts.msgs[bot_number]) > 50:
                log.warning(("Queue size for bot number {} is > 50, " +
                             "consider adding more bots").format(
                                 bot_number + 1))


def getLevel(msg):
    lvlStr = ['lvl', 'level', 'nivel']
    fields = ['title', 'description']
    lvl = 1
    for field in fields:
        for text in lvlStr:
            if text in msg[field].lower():
                lvl = int(re.search(r'\d+', msg[field].lower().split(text)[
                    1]).group())
    return lvl


async def notification(client, message, bot_number):
    return
    msg = message.embeds[0]
    made = False
    if 'egg' in msg['title']:
        egg = True
    else:
        egg = False
        pokemon = next(pokemon for pokemon in dicts.pokemon if pokemon in msg[
            'title'].lower().replace('nidoran♀', 'nidoranf').replace(
                'nidoran♂', 'nidoranm'))
    lvl = getLevel(msg)
    if args.areas != []:
        try:
            area = next(area for area in args.areas if area in msg[
                'description'].lower())
        except:
            log.error('PokeAlarm embed does not have a recognized area or ' +
                      'geofence in the description')
    for user in list(dicts.users[bot_number]):
        if (dicts.users[bot_number][user]['paused'] is False and
            (args.areas == [] or
             area in dicts.users[bot_number][user]['areas']) and
            ((egg is False and
              pokemon in dicts.users[bot_number][user]['pokemon']) or
             (dicts.users[bot_number][user]['eggs'] is not None and
              egg is True and lvl >= dicts.users[bot_number][user]['eggs']) or
             (dicts.users[bot_number][user]['raids'] is not None and
              egg is False and lvl >= dicts.users[bot_number][user][
                  'raids']))):
            if made is False:
                try:
                    col = msg['color']
                except:
                    col = int('0x4F545C', 16)
                em = discord.Embed(title=msg['title'], url=msg['url'],
                                   description=msg['description'], color=col)
                em.set_thumbnail(url=msg['thumbnail']['url'])
                try:
                    em.set_image(url=msg['image']['url'])
                except:
                    pass
                made = True
            dicts.msgs[bot_number].append([user, em])


async def rsvp(client, reaction, user, bot_number):
    found = False
    async for message in client.logs_from(discord.utils.find(
        lambda c: c.id == args.active_raids_channel,
            client.get_all_channels())):
        if (len(message.embeds) > 0 and
                message.embeds[0]['url'] == reaction.message.embeds[0]['url']):
            msg = message
            found = True
            break
    if found is False:
        descript = (reaction.message.embeds[0]['description'] + "\n\nInterested:\n" +
                    "```\n \n```\nAt the raid:\n```\n \n```")
        try:
            col = reaction.message.embeds[0]['color']
        except:
            col = int('0x4F545C', 16)
        em = discord.Embed(title=reaction.message.embeds[0]['title'],
                           url=reaction.message.embeds[0]['url'],
                           description=descript, color=col)
        em.set_thumbnail(url=reaction.message.embeds[0]['thumbnail']['url'])
        try:
            em.set_image(url=reaction.message.embeds[0]['image']['url'])
        except:
            pass
        msg = await client.send_message(discord.utils.find(
            lambda c: c.id == args.active_raids_channel,
            client.get_all_channels()), embed=em)
    omw = []
    here = []
    descript_split = msg.embeds[0]['description'].split('```')
    omw = descript_split[1].split('\n')
    here = descript_split[3].split('\n')
    for list_ in [omw, here]:
        while '' in list_:
            list_.remove('')
        while ' ' in list_:
            list_.remove(' ')
    change = False
    if reaction.emoji == '➡':
        if user.name in omw:
            # await client.send_message(discord.utils.find(
            #     lambda u: u.id == user.id, client.get_all_members()),
            #         ("You already said you were on your way to this raid."))
            pass
        elif user.name in here:
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("That doesn't make any sense, you said you were " +
                     "already at the raid but now you are on your way?  If " +
                     "you are not actually not at the raid, please add the " +
                     ":x: reaction and try again."))
        else:
            change = True
            omw.append(user.name)
            # await client.send_message(discord.utils.find(
            #     lambda u: u.id == user.id, client.get_all_members()),
            #         ("You are on your way to a raid!"))
    elif reaction.emoji == '✅':
        if user.name in here:
            # await client.send_message(discord.utils.find(
            #     lambda u: u.id == user.id, client.get_all_members()),
            #         ("You already said you were at this gym."))
            pass
        else:
            change = True
            here.append(user.name)
            if user.name in omw:
                omw.remove(user.name)
            # await client.send_message(discord.utils.find(
            #     lambda u: u.id == user.id, client.get_all_members()),
            #         ("You have arrived at a raid!"))
    elif reaction.emoji == '❌':
        if user.name in omw:
            change = True
            omw.remove(user.name)
            # await client.send_message(discord.utils.find(
            #     lambda u: u.id == user.id, client.get_all_members()),
            #         ("You are no longer on your way to this raid!"))
        elif user.name in here:
            change = True
            here.remove(user.name)
            # await client.send_message(discord.utils.find(
            #     lambda u: u.id == user.id, client.get_all_members()),
            #         ("You are no longer at this raid!"))
        else:
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You never said you were going to this raid!"))
    else:
        # await client.send_message(discord.utils.find(
        #     lambda u: u.id == user.id, client.get_all_members()),
        #         ("That is an unrecogized reaction."))
        pass
    if change is True:
        if len(omw) == 0 and len(here) == 0:
            await client.delete_message(msg)
        else:
            if len(omw) == 0:
                omw = [' ']
            elif len(here) == 0:
                here = [' ']
            descript = descript_split[0] + '```\n'
            for reactor in omw:
                descript += reactor + '\n'
            descript += '```\nAt the raid:\n```\n'
            for reactor in here:
                descript += reactor + '\n'
            descript += '```'
            try:
                col = msg['color']
            except:
                col = int('0x4F545C', 16)
            em = discord.Embed(title=msg.embeds[0]['title'],
                               url=msg.embeds[0]['url'],
                               description=descript, color=col)
            em.set_thumbnail(url=msg.embeds[0]['thumbnail']['url'])
            try:
                em.set_image(url=msg.embeds[0]['image']['url'])
            except:
                pass
            await client.edit_message(msg, embed=em)
