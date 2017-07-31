#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import discord
import asyncio
from .utils import get_args, Dicts, update_dicts
from .notification import notification, rsvp, unrsvp
from .commands import (status, add_eggs, add_raids, add, delete_eggs,
                       delete_raids, delete, pause, pause_area, resume,
                       resume_area, subs, commands, dex, donate)

log = logging.getLogger('Bot')

args = get_args()
dicts = Dicts()
users = []


class Bot(discord.Client):

    async def on_ready(self):
        bot_number = args.bot_client_ids.index(self.user.id)
        await asyncio.sleep(bot_number)
        log.info("Bot number {} connected".format(bot_number + 1))
        await asyncio.sleep(len(args.tokens))
        if self.user.id == args.bot_client_ids[0]:
            await self.change_presence(game=discord.Game(
                name='with his pokéballs'))
        else:
            await self.change_presence(status=discord.Status.invisible)
        for server in self.servers:
            if args.muted_role is not None:
                for role in server.role_hierarchy:
                    if role.name.lower() == args.muted_role:
                        args.muted_role = role
                        break
            for member in server.members:
                if member.id not in users:
                    users.append(member.id)
        count = 0
        for user in dicts.users[bot_number]:
            if user not in users:
                dicts.users[bot_number].pop(user)
                count += 1
        if count > 0:
            update_dicts(len(args.tokens))
            log.info("Bot number {} removed {} user(s) from dicts".format(
                bot_number + 1, count))
        log.info("Bot number {} is ready".format(bot_number + 1))

    async def on_member_update(self, before, after):
        bot_number = args.bot_client_ids.index(self.user.id)
        if (args.muted_role is not None and args.muted_role in after.roles and
            int(after.id) % len(args.tokens) == bot_number and
            after.id in dicts.users[bot_number] and
                dicts.users[bot_number][after.id]['paused'] is False):
            dicts.users[bot_number][after.id]['paused'] = True
            update_dicts(len(args.tokens))
            await self.send_message(discord.utils.find(
                lambda u: u.id == after.id, self.get_all_members()),
                'Notifications have been paused for `{}`.'.format(
                    after.display_name))

    async def on_member_remove(self, member):
        bot_number = args.bot_client_ids.index(self.user.id)
        if (int(member.id) % int(len(args.tokens)) == bot_number and
                member.id in dicts.users[bot_number]):
            dicts.users[bot_number].pop(member.id)
            update_dicts(len(args.tokens))

    async def on_reaction_add(self, reaction, user):
        bot_number = args.bot_client_ids.index(self.user.id)
        if ((reaction.message.channel.id in args.feed_channels or
             reaction.message.channel.id == args.test_channel) and
                (reaction.emoji == '➡' or reaction.emoji == '✅')):
            await rsvp(self, reaction, user, bot_number)
        elif (int(user.id) % int(len(args.tokens)) == bot_number and
              (reaction.message.channel.id in args.feed_channels or
               reaction.message.channel.id == args.test_channel) and
              (reaction.emoji != '➡' and reaction.emoji != '✅')):
            await self.remove_reaction(reaction.message, reaction.emoji, user)
            await self.send_message(discord.utils.find(
                lambda u: u.id == user.id, self.get_all_members()),
                'That is an unrecogized reaction, `{}`.'.format(
                    user.display_name))

    async def on_reaction_remove(self, reaction, user):
        bot_number = args.bot_client_ids.index(self.user.id)
        if ((reaction.message.channel.id in args.feed_channels or
             reaction.message.channel.id == args.test_channel) and
                (reaction.emoji == '➡' or reaction.emoji == '✅')):
            await unrsvp(self, reaction, user, bot_number)

    async def on_message(self, message):
        bot_number = args.bot_client_ids.index(self.user.id)
        if message.channel.id in args.feed_channels and message.content == '':
            await notification(self, message, bot_number)
        elif ('%status' == message.content.lower() and
                message.channel.is_private is not True):
            await status(self, message, bot_number + 1)
        elif int(message.author.id) % int(len(args.tokens)) == bot_number:
            if ((message.channel.id == args.subscription_channel or
                 message.channel.id == args.test_channel) and
                    '%add egg' == message.content[0:8].lower()):
                await add_eggs(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  '%add raid' == message.content[0:9].lower()):
                await add_raids(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  '%add ' == message.content[0:5].lower()):
                await add(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  ('%delete egg' == message.content[0:11].lower() or
                   '%remove egg' == message.content[0:11].lower() or
                   '%gtfo egg' == message.content[0:9].lower())):
                await delete_eggs(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  ('%delete raid' == message.content[0:12].lower() or
                   '%remove raid' == message.content[0:12].lower() or
                   '%gtfo raid' == message.content[0:10].lower())):
                await delete_raids(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  ('%delete ' == message.content[0:8].lower() or
                   '%remove ' == message.content[0:8].lower() or
                   '%gtfo ' == message.content[0:6].lower())):
                await delete(self, message, bot_number)
            elif (message.channel.is_private is False and
                  ('%pause' == message.content.lower() or
                   '%p' == message.content.lower())):
                await pause(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  '%pause ' == message.content[0:7]):
                await pause_area(self, message, bot_number)
            elif (message.channel.is_private is False and
                  ('%resume' == message.content.lower() or
                   '%r' == message.content.lower())):
                await resume(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  '%resume ' == message.content[0:8]):
                await resume_area(self, message, bot_number)
            elif ((message.channel.id == args.subscription_channel or
                   message.channel.id == args.test_channel) and
                  '%subs' == message.content[0:5]):
                await subs(self, message, bot_number)
            elif ('%dex ' == message.content[0:5].lower()):
                await dex(self, message)
            elif ('%commands' == message.content.lower() or
                    '%help' == message.content.lower()):
                await commands(self, message)
            elif '%donate' == message.content.lower():
                await donate(self, message)
