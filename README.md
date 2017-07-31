# GymBot

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg) ![License](https://img.shields.io/github/license/tallypokemap/GymBot.svg) [![Build Status](https://travis-ci.org/tallypokemap/GymBot.svg?branch=master)](https://travis-ci.org/tallypokemap/GymBot) [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](paypal.me/dneal12) [![Donate](https://img.shields.io/badge/Donate-Patreon-green.svg)](patreon.com/dneal12)

A gym notification Discord bot.

For support, join this Discord server: https://discord.gg/NkcAmM5

**Requirements:**

1. Python3
2. At least one Discord bot user named "Professor Willow".  Here is a link on how to set it up: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
3. A working implementation of PokeAlarm v3.2 with PR #392. [if you want subscription commands]
4. A working implementation of RocketMap with gym-info set to `True`. [if you want scoreboard functionality]

**How to install (for Windows):**

1. `git clone https://github.com/tallypokemap/GymBot.git`
2. `cd ./GymBot`
3. `python3 -m pip install -r requirements.txt`

![](http://i.imgur.com/urOfgEn.png)

**How to set up (always use Notepad++ and never notepad!):**

*If you only want the `%dex` command:*

1. Rename `config.ini.example` to `config.ini` in the config folder.
2. Set the `tokens` variable in the config file.

*If you want subscription commands:*

1. Rename `users.json.example` to `users.json` in the dicts folder.
2. Add three more bots named "Candela", "Blanche", and "Spark" in the `tokens` variable in the config file.
3. Set the `feed_channels`, `subscription_channel`, and `areas` variables in the config file.
4. PokeAlarm's username should be `<new_team_leader>`.
5. PokeAlarm's title should have `<new_team>` somewhere in the title.
6. PokeAlarm's description should have `<gym_name>` in the first line and `<geofence>` somewhere in the third line.

*If you want scoreboard functionality:*

1. Rename `gyms.json.example` to `gyms.json` in the dicts folder.
2. Set another webhook in RocketMap.
3. Copy your gefences.txt file from PokeAlarm to the config folder.
4. Set the `scoreboard_channel`, `areas`, `host`, and `port` variables in the config file.
* Note: gym names will show up as `unknown` until the next time they fall unless you dump your RM db.
* Note: Scoreboard updates every 30 seconds.  

**TO-DO:**

* Rate Limit defense
* Delete members who left the server on start-up
* Gym Fallen Notifcation"# ProfessorWillow" 
