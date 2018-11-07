class NotStreamingException(EnvironmentError):

    def __init__(self):
        self.message = 'No stream data found. Are you sure you\'re streaming?'
        super(EnvironmentError, self).__init__(self.message)


class GameNotFoundException(IndexError):

    def __init__(self, message="Couldn't find game"):
        self.message = message
        super(IndexError, self).__init__(self.message)

class FormatException(ValueError):

    def __init__(self, expected_format):
        self.message = "Command format error: Expected format -> {}".format(expected_format)
        super(ValueError, self.message).__init__(self.message)