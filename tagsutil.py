import config

SUB_PLAN_KEY = "msg-param-sub-plan-name"
MSG_ID_KEY = "msg-id"
SUB_MONTH_KEY = "msg-param-months"
DISPLAY_NAME_KEY = "display-name"
IS_MOD_KEY = "mod"
BADGES_KEY = "badges"
BADGE_BROADCASTER_KEY = "broadcaster"


def get_message(message):
    search_string = config.CHAN + " :"
    if not search_string in message:
        return None
    result_message = message.split(search_string)
    print("Result Message: " + result_message.__str__())
    result_message = result_message[-1]
    return result_message

def _get_tags_list(message):
    tags = message.split(":")
    print("Split: " + tags.__str__() + "\n")
    tags = tags[0]
    tags = tags[1:]
    tags = tags.split(';')
    return tags        

def get_tags_dict(message):
    tag_list = _get_tags_list(message)
    print("Tag List: " + tag_list.__str__() + "\n\n")
    result_dict = dict()
    index = 0
    for tag_pair in tag_list:
        tag = tag_pair.split('=')
        if len(tag) < 2:
            result_dict[tag[0]] = None
        else:
            result_dict[tag[0]] = tag[1]
    print("Tag Dict: " + result_dict.__str__())
    return result_dict

def get_badges_from_tags(tags):
    badges_raw = tags[BADGES_KEY]
    badge_pairs = badges_raw.split(',')
    badge_dictionary = dict()
    for pair in badge_pairs:
        kvp = pair.split('/')
        badge_dictionary[kvp[0]] = kvp[1]
    return badge_dictionary
