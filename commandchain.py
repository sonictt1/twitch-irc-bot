import chatmessagecommandchain
import usernoticecommandchain
import re
import config
import tagsutil

MESSAGE_COMMAND = "PRIVMSG"
USERSTATE_COMMAND = "USERNOTICE"
tags_reg_exp = r"[^@;=]+"

class ChatResponsibilityLink(object):

    def __init__(self, successor=None):
        self.successor = successor

    def can_handle(self, message):
        raise NotImplementedError

    def handle(self, message, net_socket):
        if not self.can_handle(message):
            if self.successor:
                self.successor.handle(message, net_socket)
            return
        self.do_stuff(message, net_socket)

    def do_stuff(self, message, net_socket):
        raise NotImplementedError

class ChatMessageLink(ChatResponsibilityLink):

    def __init__(self, successor=None):
        super().__init__(successor=successor)

    def can_handle(self, message):
        return MESSAGE_COMMAND in message

    def do_stuff(self, message, net_socket):
        tags = tagsutil.get_tags_dict(message)
        badges = tagsutil.get_badges_from_tags(tags)
        user_message = tagsutil.get_message(message)
        username = tags[tagsutil.DISPLAY_NAME_KEY]
        is_broadcaster = False
        is_mod = False
        print("Badges {}".format(badges.keys()))
        if(tagsutil.BADGE_BROADCASTER_KEY in badges.keys()):
            print("Is broadcaster")
            print("Broadcaster value {}".format(badges[tagsutil.BADGE_BROADCASTER_KEY]))
            is_broadcaster = badges[tagsutil.BADGE_BROADCASTER_KEY] == "1"
        is_mod = False
        if(tagsutil.IS_MOD_KEY in tags.keys()):
            is_mod = tags[tagsutil.IS_MOD_KEY] == "1"
        is_authed = is_broadcaster or is_mod
        print("Is authed {}".format(is_authed))
        print(username + ": " + user_message + "\n\n")
        self.recognize_command(user_message, username, net_socket, is_authed)

    def recognize_command(self, message, username, net_socket, is_mod):
        remove_command_link = chatmessagecommandchain.RemoveDictCommandLink()
        add_command_link = chatmessagecommandchain.AddDictCommandLink(successor=remove_command_link)
        game_link = chatmessagecommandchain.GameInfoLink(successor=add_command_link)
        dict_link = chatmessagecommandchain.DictLink(successor=game_link)
        dict_link.handle(username, message, net_socket, is_mod=is_mod)
        
class UserEventLink(ChatResponsibilityLink):

    def __init__(self, successor=None):
        super().__init__(successor=successor)

    def can_handle(self, message):
        return USERSTATE_COMMAND in message

    def do_stuff(self, message, net_socket):
        sub_link = usernoticecommandchain.SubOrResubCommandLink()
        sub_link.handle(message, net_socket)
     
        
    