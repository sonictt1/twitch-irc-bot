import config
from apis import APIS
import exceptions
from chat import Chat
from chatdecorators import TimeToBeatDecorator
class Game:

    def __init__(self):

        json = None
        self.summary = None
        self.url = None
        self.beat_time = None
        self.game_chat = None
        try:
            self.api = APIS()
            json = self.api.get_game_info()
            print(json)
            self.name = json['name']
            if 'summary' in json:
                self.summary = json['summary'].replace('\n', ' ')
                if len(self.summary) > 400:
                    self.summary = self.summary[:400] + '... '
            else:
                self.summary = None
            self.url = json['url']
            self.beat_time = self._get_times_to_beat(json)
            self.game_chat = Chat('@{} is playing {}. '.format(config.USERNAME, self.name))
        except exceptions.NotStreamingException:
            raise exceptions.NotStreamingException()
        except exceptions.GameNotFoundException:
            raise exceptions.GameNotFoundException(message=APIS().get_game_streaming())



    def _get_times_to_beat(self, game_json):
        if 'time_to_beat' in game_json:
            time_to_beat = game_json['time_to_beat']
            print(time_to_beat)
            time_to_beat_normal = None
            time_to_beat_haste = None
            time_to_beat_complete = None
            if 'normally' in time_to_beat:
                time_to_beat_normal = time_to_beat['normally']
                time_to_beat_normal = time_to_beat_normal / (60*60)

            if 'completely' in time_to_beat:
                time_to_beat_complete = time_to_beat['completely']
                time_to_beat_complete = time_to_beat_complete / (60*60)

            if 'hastly' in time_to_beat:
                time_to_beat_haste = time_to_beat['hastly']
                time_to_beat_haste = time_to_beat_haste / (60*60)

            return BeatTime(time_to_beat_haste, time_to_beat_normal, time_to_beat_complete)

class BeatTime:

    def __init__(self, haste_time, normal_time, completionist_time):
        self.hastily = haste_time
        self.normal = normal_time
        self.completionist = completionist_time

    def is_empty(self):
        return not self.hastily and not self.normal and not self.completionist
