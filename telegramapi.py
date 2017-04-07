import requests


def get_string(field, data, default=""):
    if field in data:
        return data[field]
    else:
        return default


def get_int(field, data, default=0):
    if field in data:
        return int(data[field])
    else:
        return default


def get_bool(field, data, default=False):
    if field in data:
        return bool(data[field])
    else:
        return default


class TelegramApi:

    Updates = []

    class User:
        def __init__(self, data):
            self.Id = int(data['id']);
            self.FirstName = data['first_name']
            self.LastName = get_string('last_name', data)
            self.Username = get_string('username', data)

        def to_string(self):
            return 'USER: ' + str(self.Id) + ' ' + self.FirstName + ' ' + self.LastName + ' ' + self.Username

        def print(self):
            print(self.to_string() + '\n')

    class Chat:
        def __init__(self, data):
            self.Id = int(data['id'])
            self.Type = data['type']
            self.Title = get_string('title', data)
            self.FirstName = get_string('first_name', data)
            self.LastName = get_string('last_name', data)
            self.Username = get_string('username', data)
            self.Every1Admin = get_bool('all_members_are_administrators', data)

        def to_string(self):
            return 'CHAT: ' + str(self.Id) + ' ' + self.Type + ' ' + self.Title + ' ' + self.FirstName

        def print(self):
            print(self.to_string() + '\n')

    class Message:
        def __init__(self, data):
            self.Id = int(data['message_id'])
            self.User = TelegramApi.User(data['from']) if 'from' in data else None
            self.Date = get_int('date', data, -1)
            self.Chat = TelegramApi.Chat(data['chat'])
            self.Text = get_string('text', data, '')

        def has_user(self) -> bool:
            return self.User is not None

        def to_string(self):
            return 'MESSAGE: ' + str(self.Id) + ' ' + self.User + ' ' + self.Text

        def print(self):
            print(self.to_string() + '\n')

    class Update:
        def __init__(self, data):
            self.Id = int(data['update_id'])
            self.Message = TelegramApi.Message(data['message']) if 'message' in data else None

        def has_message(self) -> bool:
            return self.Message is not None

        def to_string(self):
            return 'Update: ' + str(self.Id)

        def print(self):
            print(self.to_string() + '\n')

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.telegram.org/bot" + self.api_key + "/"

    def send_mess(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url + 'sendMessage', data=params)
        return response

    def _parse_updates(self, updatejson):
        if 'ok' not in updatejson:
            return False

        ok = bool(updatejson['ok'])

        if not ok:
            return False

        updates_json = updatejson['result']

        for upd in updates_json:
            self.Updates.append(TelegramApi.Update(upd))

        return True

    def get_updates(self, offset=0):
        req = self.url + 'getUpdates' + (('?offset=' + str(offset)) if offset != 0 else '')
        response = requests.get(req)
        return self._parse_updates(response.json())

    def add_updates(self, json_data):
        return self._parse_updates(json_data)