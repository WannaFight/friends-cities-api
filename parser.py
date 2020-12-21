from os import getenv

# from googletrans import Translator
import vk


VK_TOK = getenv('VK_TOKEN')
API_V = 5.122

session = vk.Session(access_token=VK_TOK)
api = vk.API(session, lang='ru', v=API_V)
# tr = Translator()


# Suspended due to low speed
# def translate(word: str, lang):
#     """Translate to specified language (default=Russian).
#     If word is empty - return 'City not specified'
#     """
#     word = "Город не указан" if not word else word

#     try:
#         return tr.translate(word, dest=lang).text \
#             if tr.detect(word).lang != lang \
#             else word
#     # Anything can go wrong :(
#     except:
#         return word


def get_response(target_id):
    """
    :param target_id: vk id of target https://vk.com/ID

    :returns: JSON with results {'code': code, 'content': [...]}
    """

    json_resp = {'code': 200, 'content': []}

    try:
        target_id = api.users.get(user_ids=target_id)[0]['id']
        friends_data = api.friends.get(user_id=target_id,
                                       fields=['city', 'home_town'])['items']
    except vk.exceptions.VkAPIError as e:
        json_resp['code'] = e.code
        json_resp['content'].append({'message': e.message})

        return json_resp

    if not friends_data:
        text = f"User https://vk.com/id{target_id} has no friends."
        json_resp['code'] = 204
        json_resp['content'].append({'message': text})

        return json_resp

    for friend in friends_data:
        # city = translate(friend.pop('city', {}).pop('title', ''), lang)
        # home_town = translate(friend.get('home_town', ''), lang)
        city = friend.pop('city', {}).pop('title', 'City is not specified')
        home_town = friend.get('home_town', '') \
            if friend.get('home_town', '') else 'City is not specified'
        vk_id = friend.get('id')

        json_resp['content'].append({'user': f"https://vk.com/id{vk_id}",
                                     'current_city': city,
                                     'home_city': home_town})
    # for sub_friends in chunk(friends_data, 4):
    #     thread = Thread(target=get_cities, args=(sub_friends, lang))
    #     thread.start()

    return json_resp
