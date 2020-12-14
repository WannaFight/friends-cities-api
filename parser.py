from getpass import getuser
from os import getenv, environ

from textblob import TextBlob, exceptions
import vk


# Get token from env vars if app is running from heroku
VK_TOK = (open(f"/home/{getuser()}/Documents/access_token.txt").read(),
          getenv("VK_TOKEN"))['DYNO' in environ]
API_V = 5.122


def translate_names(word: TextBlob, lang='ru'):
    """Translate to specified language (default=Russian).
    If word is empty - return 'City is not defined'
    If it was not translated - return as it is.
    """
    try:
        if word:
            if word.detect_language() != lang:
                return word.translate(to=lang).string
            else:
                return word.title().string
        else:
            return "Город не указан"
    except exceptions.NotTranslated:
        return word.string


def get_friends_cities(target_id):
    """
    :param target_id: vk id of target https://vk.com/ID

    :returns: JSON with results {'code': code, 'content': [...]}
    """
    session = vk.Session(access_token=VK_TOK)
    api = vk.API(session, lang='ru', v=API_V)
    json_resp = {'code': 200, 'content': []}

    try:
        target_id = api.users.get(user_ids=target_id)[0]['id']
        friends_ids = api.friends.get(user_id=target_id)['items']
    except vk.exceptions.VkAPIError as e:
        json_resp['code'] = e.code
        json_resp['content'].append({'message': e.message})

        return json_resp

    if not friends_ids:
        text = f" User https://vk.com/id{target_id} has no friends."
        json_resp['code'] = 204
        json_resp['content'].append({'message': text})

        return json_resp

    for friend_id in friends_ids:
        resp = api.users.get(user_id=friend_id,
                             fields=['city', 'home_town'])[0]
        city = translate_names(TextBlob(
                               dict(resp.pop('city', '')).pop('title', '')))
        home_town = translate_names(TextBlob(resp.get('home_town', '')))

        json_resp['content'].append({'user': f"https://vk.com/id{friend_id}",
                                     'current_city': city,
                                     'home_city': home_town})

    return json_resp
