class Chat:

    def __init__(self, text=""):
        self.text = text
        self.decorators = []

    def add_decorator(self, chat_decorator):
        self.decorators.append(chat_decorator)

    def get_chat_text(self):
        chat_str = self.text
        for decorator in self.decorators:
            chat_str = decorator.decorate_chat(chat_str)
        return chat_str
