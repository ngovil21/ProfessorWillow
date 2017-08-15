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


async def send_dm(client, user, msg=None, emb=None, count=1):
    try:
        await client.send_message(discord.utils.find(
            lambda u: u.id == user, client.get_all_members()), msg,
                                  embed=emb)
    except Exception as e:
        if count < 3:
            await asyncio.sleep(5)
            await send_dm(client, user, msg=msg, emb=emb, count=count + 1)
        else:
            log.error(('Faild to send: To {} due to Discord rate ' +
                      'limits or the end-user blocking the bot').format(
                          discord.utils.find(lambda u: u.id == user,
                              client.get_all_members()).display_name),
                      e.__class__.__name__, e)


async def notification(client, message, bot_number):
    msg = message.embeds[0]
    made = False
    if 'egg' in msg['title']:
        egg = True
    else:
        egg = False
        pokemon = next(pokemon for pokemon in dicts.pokemon if pokemon in msg[
            'title'].lower().replace('nidoran♀', 'nidoranf').replace(
                'nidoran♂', 'nidoranm'))
    if 'lvl' in msg['title'].lower():
        lvl = int(re.search(r'\d+', msg['title'].lower().split('lvl')[
            1]).group())
    elif 'lvl' in msg['description'].lower():
        lvl = int(re.search(
            r'\d+', msg['description'].lower().split('lvl')[1]).group())
    elif 'level' in msg['title'].lower():
        lvl = int(re.search(r'\d+', msg['title'].lower().split('level')[
            1]).group())
    elif 'level' in msg['description'].lower():
        lvl = int(re.search(
            r'\d+', msg['description'].lower().split('level')[1]).group())
    else:
        lvl = 1
    if args.areas != []:
        try:
            area = next(area for area in args.areas if area in msg[
                'description'].lower())
        except:
            log.error('PokeAlarm embed does not have a recognized area or ' +
                      'geofence in the description')
    for user in dicts.users[bot_number]:
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
            await send_dm(client, user, emb=em)


async def rsvp(client, reaction, user, bot_number):
    found = False
    async for message in client.logs_from(discord.utils.find(
        lambda c: c.id == args.active_raids_channel,
            client.get_all_channels())):
        if message.embeds[0]['url'] == reaction.message.embeds[0]['url']:
            msg = message
            found = True
            break
    if found is False:
        descript = (reaction.message.embeds[0]['description'] + "\n\nOn " +
                    "their way:``` ```At the raid:``` ```")
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
    omw = descript_split[1].lstrip().split('\n')
    here = descript_split[3].lstrip().split('\n')
    change = False
    if reaction.emoji == '➡':
        if user.name in omw:
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                                      ("You already said you were on your " +
                                       "way to this raid."))
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
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You are on your way to a raid!"))
    elif reaction.emoji == '✅':
        if user.name in here:
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You already said you were at this gym."))
        else:
            change = True
            here.append(user.name)
            if user.name in omw:
                omw.remove(user.name)
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You have arrived at a raid!"))
    elif reaction.emoji == '❌':
        if user.name in omw:
            change = True
            omw.remove(user.name)
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You are no longer on your way to this raid!"))
        elif user.name in here:
            change = True
            here.remove(user.name)
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You are no longer at this raid!"))
        else:
            await client.send_message(discord.utils.find(
                lambda u: u.id == user.id, client.get_all_members()),
                    ("You never said you were going to this raid!"))
    else:
        await client.send_message(discord.utils.find(
            lambda u: u.id == user.id, client.get_all_members()),
                ("That is an unrecogized reaction."))
    if change is True:
        if len(omw) == 1 and len(here) == 1:
            await client.delete_message(msg)
        else:
            if len(omw) == 1:
                omw = [' ']
            if len(here) == 1:
                here = [' ']
            descript = descript_split[0] + '```'
            for reactor in omw:
                descript += reactor + '\n'
            descript += '```At the raid:```'
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
