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
            send_dm(client, user, msg=msg, emb=emb, count=count + 1)
        else:
            log.error(('Faild to send: {} gym to {} due to Discord rate ' +
                      'limits or the end-user blocking the bot').format(
                          dicts.team[client.user.name], discord.utils.find(
                              lambda u: u.id == user,
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
            (pokemon in dicts.users[bot_number][user]['pokemon'] or
             (egg is True and lvl >= dicts.users[bot_number][user]['eggs']) or
             (egg is False and lvl >= dicts.users[bot_number][user][
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
    msg = reaction.message.embeds[0]
    omw = []
    here = []
    for react in reaction.message.reactions:
        users = await client.get_reaction_users(react)
        for user_ in users:
            if react.emoji == '➡':
                omw.append(user_)
            elif react.emoji == '✅':
                here.append(user_)
    if reaction.emoji == '➡' and user in here:
        await client.remove_reaction(reaction.message, reaction.emoji, user)
        await client.send_message(discord.utils.find(
            lambda u: u.id == user.id, client.get_all_members()),
            "That doesn't make any sense `{}`, you said you were already " +
            "at teh raid but now you are on your way?  If you are not " +
            "actually not at the raid, please remove your first reaction " +
            "and try again".format(user.display_name))
    else:
        omw = list(set(omw) - set(here))
        descript = msg['description'] + '\n'
        if omw != []:
            descript += "\nOn their way:\n```"
            for reactor in omw:
                descript += reactor.display_name + '\n'
            descript += '```'
        if here != []:
            descript += '\nAt the gym:\n```'
            for reactor in here:
                descript += reactor.display_name + '\n'
            descript += '```'
        try:
            col = msg['color']
        except:
            col = int('0x4F545C', 16)
        em = discord.Embed(title=msg['title'], url=msg['url'],
                           description=descript, color=col)
        em.set_thumbnail(url=msg['thumbnail']['url'])
        try:
            em.set_image(url=msg['image']['url'])
        except:
            pass
        for user_ in list(set(omw + here)):
            if user_ == user:
                if reaction.emoji == '➡':
                    dm = "You are on you way to a raid!\n\n"
                else:
                    dm = "You have arrived at a raid!\n\n"
            else:
                if reaction.emoji == '➡':
                    dm = ("`{}` is on their way to the " +
                          "raid!\n\n").format(user.display_name)
                else:
                    dm = "`{}` has arrived at the raid!\n\n".format(
                        user.display_name)
            await send_dm(client, user_.id, msg=dm, emb=em)


async def unrsvp(client, reaction, user, bot_number):
    msg = reaction.message.embeds[0]
    omw = []
    here = []
    for react in reaction.message.reactions:
        users = await client.get_reaction_users(react)
        for user_ in users:
            if react.emoji == '➡':
                omw.append(user_)
            elif react.emoji == '✅':
                here.append(user_)
    if reaction.emoji == '➡' and user in here:
        pass
    else:
        omw = list(set(omw) - set(here))
        descript = msg['description'] + '\n'
        if omw != []:
            descript += "\nOn their way:\n```"
            for reactor in omw:
                descript += reactor.display_name + '\n'
            descript += '```'
        if here != []:
            descript += '\nAt the gym:\n```'
            for reactor in here:
                descript += reactor.display_name + '\n'
            descript += '```'
        try:
            col = msg['color']
        except:
            col = int('0x4F545C', 16)
        em = discord.Embed(title=msg['title'], url=msg['url'],
                           description=descript, color=col)
        em.set_thumbnail(url=msg['thumbnail']['url'])
        try:
            em.set_image(url=msg['image']['url'])
        except:
            pass
        for user_ in list(set(omw + here)):
            if user_ == user:
                if reaction.emoji == '➡':
                    dm = "You are no longer on you way to a raid!\n\n"
                else:
                    dm = "You are no longer at a raid!\n\n"
            else:
                if reaction.emoji == '➡':
                    dm = ("`{}` is no longer on their way to the " +
                          "raid!\n\n").format(user.display_name)
                else:
                    dm = "`{}` is no longer at the raid!\n\n".format(
                        user.display_name)
            await send_dm(client, user_.id, msg=dm, emb=em)
