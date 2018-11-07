import chatdecorators
import chatcommands
import chat
import tagsutil

class ChatMessageCommandChain(object):

    def __init__(self, successor=None):
        self.successor = successor

    def can_handle(self, message, tags):
        raise NotImplementedError

    def handle(self, message, net_socket):
        tags = tagsutil.get_tags_dict(message)
        if not self.can_handle(message, tags):
            if self.successor:
                self.successor.handle(username, message, net_socket)
            return
        self.do_stuff(tags[tagsutil.DISPLAY_NAME_KEY], message, net_socket, tags)

    def do_stuff(self, username, message, net_socket, tags):
        raise NotImplementedError

class SubOrResubCommandLink(ChatMessageCommandChain):

    def can_handle(self, message, tags):
        if not tagsutil.MSG_ID_KEY in tags.keys():
            return False
        message_id = tags[tagsutil.MSG_ID_KEY]
        return message_id == "resub" or message_id == "sub"

    def do_stuff(self, username, message, net_socket, tags):
        is_resub = tags[tagsutil.MSG_ID_KEY] == "resub"
        chat_obj = chat.Chat()
        chat_obj.add_decorator(chatdecorators.SubOrResubDecorator(username, tags[tagsutil.SUB_MONTH_KEY], tags[tagsutil.SUB_PLAN_KEY].replace("\s", " "), is_resub))
        chatcommands.chat(net_socket, chat_obj.get_chat_text())