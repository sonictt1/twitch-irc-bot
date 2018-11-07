import chat
import chatdecorators
import chatcommands
import config
import exceptions
import json
import os
import re
from apiobjects import Game

WHITESPACE_RE = r" +"

class ChatMessageCommandChain(object):

    def __init__(self, successor=None):
        self.successor = successor

    def can_handle(self, message):
        raise NotImplementedError

    def is_priviliged(self):
        return False

    def handle(self, username, message, net_socket, is_mod=False):
        if not self.can_handle(message):
            if self.successor:
                self.successor.handle(username, message, net_socket, is_mod)
            return
        elif self.is_priviliged() and not is_mod:
            print("Is not privilidged user. Is user {} a mod?".format(username))
            return
            
        self.do_stuff(username, message, net_socket)

    def do_stuff(self, username, message, net_socket):
        raise NotImplementedError

class GameInfoLink(ChatMessageCommandChain):

    def __init__(self, successor=None):
        super().__init__(successor=successor)

    def can_handle(self, message):
        return '!game' in message

    def do_stuff(self, username, message, net_socket):
        self.get_game_info(net_socket, message, username)

    def get_game_info(self, sock, msg, username):
        game = None
        try:
            game = Game()
            print(game.__str__())
        except exceptions.NotStreamingException as e:
            chat_obj = chat.Chat("@{} isn't streaming right now!".format(config.USERNAME))
            chat_obj.add_decorator(chatdecorators.UsernamePrefixDecorator(username))
            chatcommands.chat(sock, chat_obj.get_chat_text())
            return
        except exceptions.GameNotFoundException as e:
            chat_obj = chat.Chat("We couldn't find \"{}\" in the IGDB database. Want to help out? Add it to the database! https://www.igdb.com/".format(e.message))
            chat_obj.add_decorator(chatdecorators.UsernamePrefixDecorator(username))
            chatcommands.chat(sock, chat_obj.get_chat_text())
            return
        except Exception as e:
            chat_obj = chat.Chat("Weird, something else went wrong.")
            chat_obj.add_decorator(chatdecorators.UsernamePrefixDecorator(username))
            chatcommands.chat(sock, chat_obj.get_chat_text())
            return
        print(game.__str__())
        if game:
            chat_obj = chat.Chat()
            msg = msg.replace("\r", "")
            msg = msg.replace("\n", "")
            args = re.split(WHITESPACE_RE, msg)
            args.pop(0)
            if not args:
                chat_obj.add_decorator(chatdecorators.SummaryDecorator(game))
            elif "summary" in args:
                chat_obj.add_decorator(chatdecorators.SummaryDecorator(game))
            elif "beat-time" in args:
                chat_obj.add_decorator(chatdecorators.TimeToBeatDecorator(game))
        print(game.__str__())
        chat_obj.add_decorator(chatdecorators.URLDecorator(game))
        chat_obj.add_decorator(chatdecorators.UsernamePrefixDecorator(username))
        chatcommands.chat(sock, chat_obj.get_chat_text())

class DictLink(ChatMessageCommandChain):

    def __init__(self, successor=None):
        super().__init__(successor=successor)
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json') as commands_file:
            self.commands = json.load(commands_file)
        self.command = None
        

    def can_handle(self, message):
        self.command = self._find_matching_command(message, self.commands)
        if self.command:
            return True
        return False

    def do_stuff(self, username, message, net_socket):
        text = self.commands[self.command]
        chat_obj = chat.Chat()
        chat_obj.add_decorator(chatdecorators.DictDecorator(text))
        chatcommands.chat(net_socket, chat_obj.get_chat_text())

    def _find_matching_command(self, message, commands):
        for command in commands.keys():
            if command.lower() in message.lower():
                return command
        return None


class AddDictCommandLink(ChatMessageCommandChain):

    def __init__(self, successor=None):
        super().__init__(successor=successor)
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json') as commands_file:
            self.commands = json.load(commands_file)
        self.command = None
        
    def is_priviliged(self):
        return True

    def can_handle(self, message):
        return "!add" in message and "=" in message

    def do_stuff(self, username, message, net_socket):
        command_to_add = message.replace("!add", "")
        split_pair = command_to_add.split("=")
        chat_obj = chat.Chat()
        if len(split_pair) != 2:
            exception = exceptions.FormatException("command = response")
            user_decorator = chatdecorators.UsernamePrefixDecorator(username)
            exception_decorator = chatdecorators.ExceptionDecorator(exception)
            chat_obj.add_decorator(user_decorator)
            chat_obj.add_decorator(exception_decorator)
            chatcommands.chat(net_socket, chat_obj.get_chat_text)
            return
        split_pair[0] = split_pair[0].strip()
        split_pair[1] = split_pair[1].strip()
        text = self.commands["!{}".format(split_pair[0])] = split_pair[1]
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json', 'w') as commands_file:
            commands_file.write(json.dumps(self.commands))
        chat_obj.add_decorator(chatdecorators.DictDecorator("Added command !{}".format(split_pair[0])))
        chatcommands.chat(net_socket, chat_obj.get_chat_text())

class RemoveDictCommandLink(ChatMessageCommandChain):

    def __init__(self, successor=None):
        super().__init__(successor=successor)
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json') as commands_file:
            self.commands = json.load(commands_file)
        self.command = None
        
    def is_priviliged(self):
        return True

    def can_handle(self, message):
        return "!remove" in message

    def do_stuff(self, username, message, net_socket):
        command_to_remove = message.replace("!remove", "")
        command_to_remove = command_to_remove.strip()
        print("Remove: {}".format(command_to_remove))
        if(not "!" in command_to_remove):
            command_to_remove = "!{}".format(command_to_remove)
        print("command keys: {}".format(self.commands.keys()))
        if(not command_to_remove in self.commands.keys()):
            chat_obj = chat.Chat("Command {} not found in command list".format(command_to_remove))
            chatcommands.chat(net_socket, chat_obj.get_chat_text())
            return
        self.commands.pop(command_to_remove)
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json', 'w') as commands_file:
            commands_file.write(json.dumps(self.commands))
        chat_obj = chat.Chat("Removed command {}".format(command_to_remove))
        chatcommands.chat(net_socket, chat_obj.get_chat_text())