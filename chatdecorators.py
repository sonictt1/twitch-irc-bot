import json

class ChatDecorator(object):

    def decorate_chat(self):
        raise NotImplementedError

class SummaryDecorator(ChatDecorator):
    def __init__(self, game):
        self.summary = game.summary

    def decorate_chat(self, chat_text):
        if not self.summary or self.summary == "":
            return 'No summary found in IGDB.'
        result_summary=self.summary
        if len(self.summary) > 100:
            result_summary = self.summary[0:99]
            result_summary += "..."
        return  chat_text + result_summary

class TimeToBeatDecorator(ChatDecorator):

    def __init__(self, game):
        ChatDecorator.__init__(self)
        self.beat_time = game.beat_time

    def decorate_chat(self, chat_text):
        if not self.beat_time or self.beat_time.is_empty():
            return ' No data found for beat time in IGDB'

        average_str = ''
        completionist_str = ''
        hasty_str = ''

        if not self.beat_time.normal:
            average_str = ' No data found about the time to beat at an average completetion percentage. '
        else:
            average_str = ' Takes approxmiately {} hours to finish at an average completion percentage. '.format(self.beat_time.normal)

        if not self.beat_time.completionist:
            completionist_str = ' No data found about the time to beat at 100%% completetion.'
        else:
            completionist_str = ' Takes approxmiately {} hours to finish at 100%% completetion.'.format(self.beat_time.completionist)

        if not self.beat_time.hastily:
            hasty_str += ' No data found about the time to beat, critical-path-only.'
        else:
            hasty_str = ' Takes approxmiately {} hours to finish critical-path.'.format(self.beat_time.hastily)

        return chat_text + hasty_str + average_str + completionist_str

class URLDecorator(ChatDecorator):

    def __init__(self, game):
        ChatDecorator.__init__(self)
        self.url = game.url

    def decorate_chat(self, chat_text):
        return chat_text + ' ' + self.url

class UsernamePrefixDecorator(ChatDecorator):

    def __init__(self, username):
        ChatDecorator.__init__(self)
        self.username = username

    def decorate_chat(self, chat_text):
        return '@' + self.username + ' -> ' + chat_text


class MotdDecorator(ChatDecorator):

    def __init__(self):
        self.TIMER_MSG_TEXT = "Thank you so much for hanging out with me! If you're enjoying the stream follows are always appreciated. Bit and Sub revenue helps fund the stream, and let's Twitch know my content is quality :) . Use !schedule or check my panels below the stream to see my normal weekly schdule. Thanks for your viewership and support! Enjoy the stream! sonictBang"

    def decorate_chat(self, chat_text):
        return chat_text + " " + self.TIMER_MSG_TEXT


class ScheduleDecorator(ChatDecorator):

    def __init__(self):
        self.SCHEDULE_MESSAGE = "Current weekly schedule is Mon (5:00PM CT - 8:00PM CT), Wed (5:00PM CT - 8:00PM CT), and Sat (1:00PM CT - 5:00PM CT)."

    def decorate_chat(self, chat_text):
        return chat_text + " " + self.SCHEDULE_MESSAGE

class DabDecorator(ChatDecorator):

    def __init__(self):
        self.DAB = "*DAB*"

    def decorate_chat(self, chat_text):
        return chat_text + " " + self.DAB

class SubOrResubDecorator(ChatDecorator):

    def __init__(self, username, sub_months, sub_plan, is_resub):
        self.sub_months = sub_months
        self.username = username
        self.sub_plan = sub_plan
        self.is_resub = is_resub

    def decorate_chat(self, chat_text):
        if not self.is_resub:
            return chat_text + " Welcome @{}! Thanks for being a {}".format(self.username, self.sub_plan)
        return chat_text + " Holy crap! Thanks @{}, for being a {} for {} months!".format(self.username, self.sub_plan, self.sub_months)

class DictDecorator(ChatDecorator):
    def __init__(self, text):
        self.new_text = text

    def decorate_chat(self, chat_text):
        return "{} {}".format(chat_text, self.new_text)
        

class ExceptionDecorator(ChatDecorator):
    def __init__(self, exception_obj):
        self.new_text = exception_obj.message

    def decorate_chat(self, chat_text):
        return "{} {}".format(chat_text, self.new_text)