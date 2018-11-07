import re
import os

"""
    Config file that holds the various passwords, urls, etc.
"""

"""
    Twitch IRC Configs
"""

""" Twitch IRC chat host. """
HOST = "irc.chat.twitch.tv"
""" Twitch IRC chat port. """
PORT = 6667
""" IRC "nickname". Must be lowercase. 
    Can be a bot account (i.e. MyBot) """
NICK = "sonictt1"
""" Twitch IRC Oauth """
PASS = os.environ["TWITCH_OAUTH_TOKEN"]
""" Twitch IRC Channel (#<username>) """
CHAN = "#sonictt1"
""" Max message rate (messages/time (s)) """
RATE = (20/30)
""" Username of streamer """
USERNAME = "sonictt1"

"""
    Twitch API Configs
"""
TWITCH_API_CLIENT_ID = os.environ['TWITCH_API_CLIENT_ID']
TWITCH_API_STREAM_INFO = "https://api.twitch.tv/kraken/streams/{}?client_id={}".format(USERNAME, TWITCH_API_CLIENT_ID)

"""
    IGDB API Key
"""
API_KEY = os.environ['IGDB_API_KEY']
IGDB_BASE_URL = "https://api-endpoint.igdb.com/"
IGDB_BASE_URL_COMPANY = "https://api-endpoint.igdb.com/companies/"
IGDB_GAME_URL = "{}games/".format(IGDB_BASE_URL)
IGDB_LIMIT = 10