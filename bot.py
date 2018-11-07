import socket

import time
import requests
import exceptions
import chatdecorators
import chat
import chatcommands
import commandchain
from apiobjects import Game
from datetime import datetime
import config

MOD_RE = r"(?:.*?\:){3}(.*)"
msg_count = 0
mod_list = None
last_msg_time = 0
newline_string = "\r\n"

def connect():
    s = socket.socket(type=socket.SOCK_STREAM)
    # s.setblocking(0)
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    return s

def timed_chat():
    intro_chat = chat.Chat()
    intro_chat.add_decorator(chatdecorators.MotdDecorator())
    chatcommands.chat(s, intro_chat.get_chat_text())
    msg_count = 0
    last_msg_time = time.time()

def start_up(sock):
    last_msg_time = time.time()
    chatcommands.request_commands(sock)

def close_and_reconnect(sock):
    sock.close()
    new_sock = connect()
    start_up(new_sock)
    return new_sock

if __name__ == '__main__':
    s = connect()
    start_up(s)
    rollover_text = ""
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "":
            print("Connection broken, reconnecting")
            s = close_and_reconnect(s)
        if response == "PING :tmi.twitch.tv\n":
            s.send("PONG :tmi.twitch.tv\n".encode("utf-8"))
        elif response == "RECONNECT :tmi.twitch.tv\n":
            s = close_and_reconnect(s)
        else:
            if newline_string in response:
                messages = response.split(newline_string)
                if rollover_text:
                    messages[0] = rollover_text + messages[0]
                    rollover_test = ""
                print("Messages: {}".format(messages))
                if not newline_string in messages[-1]:
                    rollover_text = messages[-1]
                    messages.pop(-1)
            else:
                rollover_text = response
            command = commandchain.ChatMessageLink()
            user_notice_command = commandchain.UserEventLink(successor=command)
            for message in messages:
                user_notice_command.handle(message, s)
            time.sleep(1/config.RATE)
