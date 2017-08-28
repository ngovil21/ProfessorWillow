# ProfessorWillow

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg) ![License](https://img.shields.io/github/license/friscoMad/ProfessorWillow.svg) [![Build Status](https://travis-ci.org/friscoMad/ProfessorWillow.svg?branch=master)](https://travis-ci.org/friscoMad/ProfessorWillow) [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/raparicio)


A raid notification and pokedex bot.

For support, join this Discord server: https://discord.gg/rEfST4h

**Attribution:**
This bot was developed by @tallypokemap, he did stop the development as he sold it's code and removed it from Github. I will try to maintain the bot active and under development but all the hard work was done for me, so please consider donating him: https://www.paypal.me/dneal12


**Requirements:**

1. Python3
2. Create your bot and get credentials, do not add to your server yet. Here is a link on how to set it up: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token 
3. Use this url to give the add your bot to your server with the proper permissions: https://discordapp.com/oauth2/authorize?client_id=INSERT_CLIENT_ID_HERE&scope=bot&permissions=93248


**How to install (for Windows):**

1. `git clone https://github.com/tallypokemap/ProfessorWillow.git`
2. `cd ./ProfessorWillow`
3. `python3 -m pip install -r requirements.txt`

![](http://i.imgur.com/n4gs3C9.png)

**How to set up (always use Notepad++ and never notepad!):**

1. Copy `/config/config.ini.example` to `/config/config.ini` in the config folder.
2. Set the `tokens`, `bot_client_ids`,`feed_channels`, `active_raids_channel` and any other optional variables in the config file. Check this to get the channel Ids https://support.discordapp.com/hc/en-us/articles/206346498 (it is like server but clicking on channel).
3. Copy `/dicts/user.json.example` to `/dicts/user.json` 
4. `python3 start_willow.py`
5. `%commands` if you need a list of commands.

**How does it works**

The bot will be listening to `subscription_channel` and process all commands sent to him, all commands start with `%`.

At the same time the bot will listen to `feed_channels` for PA raid/egg notifications and when a new arrives it will add reaction icons to them and if any user has configured alerts that matches it will send him a DM with the notification.
If someone click on the reactions in DM or feed the bot will post that notification to `active_raids_channel` with the name of the user and the status, other people can click on reactions to update it's status.
Finally after the raid ends the bot will delete the notification from `active_raids_channel`.