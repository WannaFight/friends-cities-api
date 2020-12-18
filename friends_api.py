from os import path

from flask import Flask, request, send_from_directory, make_response

from parser import get_friends_cities


app = Flask(__name__)
# To display cyrillic characters in terminal
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return make_response(
            {'code': 200, 'content': [{'message': "Welcome to my API"}]},
            200)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'vk.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/cities')
def get_friends_stats():
    user_url = request.args.get('user')
    lang = request.args.get('lang', 'ru')

    resp = get_friends_cities(user_url, lang)

    return make_response(resp)


if __name__ == "__main__":
    app.run()
