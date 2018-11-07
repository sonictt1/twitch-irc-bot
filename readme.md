# Unnamed Twitch Chat Bot (Bearbot?)

This is the open-source repo for one of my hobby projects, my twich chat (IRC) chat bot. Written in Python (3.5+).

This bot is not necessarily user-friendly to run. This bot is made, unapollogetically, by me, for me. If you're a streamer with little-to-no technical computer knowledge, this bot may be difficult to run, and that's ok. 

That being said, I'll make a modicum of effort to make this guide understandable for those who are merely computer literate and who may not understand developer customs (see the licensing section below). Also remember, Google is your friend.

## A note on licensing for streamers who may not be familiar

**This code is released under the GNU General Public License v3.0. You do have responsibilities if you use or modify this code. A snippet is provided as well as a source where you can read more about this license.**

```
Permissions of this copyleft license are conditioned on making available complete source code of licensed works 
and modifications under the same license or the GNU GPLv3. Copyright and license notices must be preserved. 
Contributors provide an express grant of patent rights. However, a larger work using the licensed work through 
interfaces provided by the licensed work may be distributed under different terms and without source code for 
the larger work.
```

Notably:
* You must make the source code available. If you use this source for a bot with no modifications to a code, a link in your stream panels would suffice. A !source command with a link to this repository would be appreciated too.
* If you makes changes you must make the modified code available open source under the same license. 

[You can read more about this license here.](https://choosealicense.com/licenses/lgpl-3.0/)

## How do I try it out?

Make sure you have python 3.5+. Run pip on the requirements.txt file `pip install -r requirements.txt`

In `config.py` replace all instances of `<streamer username>` with your twitch username. If your channel name and display name are different, use your channel name for the `CHAN` variable. 

You need 3 different secrets to run every feature in this bot. 

* Twitch chat OAuth
* Twitch API Client ID
* IGDB (International Games Database) API Key (This is the hard one)

### Twitch chat OAuth

This is the easiest one. [Go here](https://twitchapps.com/tmi/) and log into your twitch account. Add this value as an environment variable called: `TWITCH_OAUTH_TOKEN`.

### Twitch API Client Id

This one is more complicated. [You have to register our bot on Twitch's dev site](https://glass.twitch.tv/console/apps/create). Once you're done, that same page will have your Client ID.

### IGDB Key

This one is the worst, because it requires an account other than Twitch (either Github or an IGDB dev account). [Here's their page on getting an API key.](https://www.igdb.com/api)

## How do I add my own commands?

Simple call-and-response commands can be added with the command `!add`. Example syntax is below:

```
!add command=response
```

You can remove these commands with `!remove`.

```
!remove command
```

It's also possible to add and remove these commands by directly editing the `commands.json` file.

Commands that require anymore than parrotting with text will have to be added to the chain-of-command pattern in the `chatmessagecommandchain.py` and `commandchain.py`.

## A note on commands.json

`commands.json` won't be around forever. For v1 it was a super quick, easy way of storing commands. It doesn't require any cloud services beyond the box you're already running on. But it's also susceptible to accidentally overwriting a lot of commands if you patch carelessly, and doesn't scale well. At some point, it'll get moved to some sort of database. Relational or nonrelational, I'm not sure yet.

## Testing

Tests? What tests? LOL

Seriously though, I need to put some testing in here.