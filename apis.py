import exceptions
import config
import requests
class APIS:

    def __init__(self):
        self.header = {'user-key': config.API_KEY, 'Accept': 'application/json'}
        self.params = None

    def get_stream_json(self):
        result = requests.get(url=config.TWITCH_API_STREAM_INFO)
        return result.json()

    def get_game_streaming(self):
        json = self.get_stream_json()
        if json['stream'] is None:
            return None
        game_name = json['stream']['game']
        return game_name

    def get_game_info(self):
        game_streaming_name = self.get_game_streaming()
        if game_streaming_name is None:
            raise exceptions.NotStreamingException()
        self.set_game_name(game_streaming_name)
        game_request = requests.get(config.IGDB_GAME_URL, params=self.params, headers=self.header)
        print(game_request)
        game_json = game_request.json()
        print(game_json)
        game_index = 0
        result_json = None
        try:
            for i in range(config.IGDB_LIMIT):
                if game_json[i]['name'] == game_streaming_name:
                    result_json = game_json[i]
                    break
            if not result_json:
                raise exceptions.GameNotFoundException()
            else:
                print(result_json)
                return result_json
        except IndexError:
            raise exceptions.GameNotFoundException()


    def set_game_name(self, name):
        self.params = {
        'fields': 'name,time_to_beat,summary,url',
        'search': name,
        'limit': config.IGDB_LIMIT
        }
