from os import path

from flask import Flask, jsonify, send_from_directory

from parser import get_friends_cities


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to my api!\n"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'vk.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/cities/<string:target_id>')
def get_friends_stats(target_id):
    return get_friends_cities(target_id)


if __name__ == "__main__":
    app.run()
