from os import getenv
from time import sleep

from googletrans import Translator
import vk


VK_TOK = getenv('VK_TOKEN')
API_V = 5.122


def translate(word: str, lang):
    """Translate to specified language (default=Russian).
    If word is empty - return 'City not specified'
    """
    word = "Город не указан" if not word else word
    tr = Translator()

    try:
        return tr.translate(word, dest=lang).text \
            if tr.detect(word).lang != lang \
            else word
    # Anything can go wrong :(
    except:
        return word


def get_friends_cities(target_id, lang='ru'):
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
        text = f"User https://vk.com/id{target_id} has no friends."
        json_resp['code'] = 204
        json_resp['content'].append({'message': text})

        return json_resp

    for friend_id in friends_ids:
        resp = api.users.get(user_id=friend_id,
                             fields=['city', 'home_town'])[0]

        city = translate(dict(resp.pop('city', '')).pop('title', ''), lang)
        home_town = translate(resp.get('home_town', ''), lang)

        json_resp['content'].append({'user': f"https://vk.com/id{friend_id}",
                                     'current_city': city,
                                     'home_city': home_town})
        sleep(1)

    return json_resp
