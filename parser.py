from os import getenv

from googletrans import Translator
import vk


VK_TOK = getenv('VK_TOKEN')
API_V = 5.122

session = vk.Session(access_token=VK_TOK)
api = vk.API(session, lang='ru', v=API_V)
tr = Translator()


def get_response(target_id, lang):
    """
    :param target_id: vk id of target https://vk.com/ID
    :param lang: language to tranlate to

    :returns: JSON with results {'code': code, 'content': [...]}
    """

    json_resp = {'code': 200, 'content': []}

    # Catching VK API exceptions
    try:
        target_id = api.users.get(user_ids=target_id)[0]['id']
        friends_data = api.friends.get(user_id=target_id,
                                       fields=['city', 'home_town'])['items']
    except vk.exceptions.VkAPIError as e:
        json_resp['code'] = e.code
        json_resp['content'].append({'message': e.message})

        return json_resp

    # User with no friends
    if not friends_data:
        text = f"User https://vk.com/id{target_id} has no friends."
        json_resp['code'] = 204
        json_resp['content'].append({'message': text})

        return json_resp

    # Creating an array of translated to destination language
    # cities and home towns from friends_data
    translated_cities = tr.translate('; '.join([user.get('city', {})
                                     .get('title', 'Not specified')
                                     for user in friends_data]),
                                     dest=lang).text.split('; ')
    translated_homes = tr.translate('; '.join([user.get('home_town', '')
                                    if user.get('home_town', '')
                                    else 'Not specified'
                                    for user in friends_data]),
                                    dest=lang).text.split('; ')

    for i, friend in enumerate(friends_data):
        vk_id = friend.get('id')

        json_resp['content'].append({'user': f"https://vk.com/id{vk_id}",
                                     'current_city': translated_cities[i],
                                     'home_city': translated_homes[i]})

    return json_resp
