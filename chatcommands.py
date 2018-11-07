import config
import time

def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    message = "PRIVMSG " + config.CHAN + " :" + msg + "\n"
    print(message)
    sock.send(message.encode("utf-8"))
    time.sleep(1/config.RATE)
    return

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))
    return

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600 - 10 minutes)
    """
    chat(sock, ".timeout {}".format(user, secs))
    return

def request_commands(sock):
    sock.send("CAP REQ :twitch.tv/commands\n".encode("utf-8"))
    sock.send("CAP REQ :twitch.tv/tags\n".encode("utf-8"))

def list_mods(sock):
    chat(sock, "/mods")
    return
