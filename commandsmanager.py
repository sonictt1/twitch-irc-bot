import abc

class AbstractCommandsManager(abc.ABC):

    @abc.abstractmethod
    def is_command_in_message(self, command):
        pass

    @abc.abstractmethod
    def get_response_for_command(self, command):
        pass

    @abc.abstractmethod
    def get_command_dict(self):
        pass

    @abc.abstractmethod
    def add_command(self, command, response):
        pass

    @abc.abstractmethod
    def remove_command(self, command):
        pass

class JsonCommandsManager(AbstractCommandsManager):

    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json') as commands_file:
            self.commands = json.load(commands_file)

    def is_command_in_message(self, command):
        return command.lower() in (command_key.lower() for command_key in self.commands)

    def update_file(self):
        with open(os.path.dirname(os.path.realpath(__file__))+'/commands.json', 'w') as commands_file:
            commands_file.write(json.dumps(self.commands))

    def get_response_for_command(self, command):
        if not does_command_exist(command):
            return None
        return self.commands[command.lower()]

    def get_command_dict(self):
        return commands

    def add_command(self, command, response):
        self.commands["!{}".format(command.lower())] = response
        self.update_file()
        

    def remove_command(self, command):
        self.commands.pop(command_to_remove)
        self.update_file()
