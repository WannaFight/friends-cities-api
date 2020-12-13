from flask import Flask, jsonify, request

from parser import get_friends_cities


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to my api!\n"


@app.route('/cities/<string:target_id>')
def get_friends_stats(target_id):
    return jsonify(get_friends_cities(target_id))


if __name__ == "__main__":
    app.run()
