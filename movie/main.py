from flask import Flask, jsonify

app = Flask(__name__)
movies = [
    {
        'name': '12 Angry Men',
        'year': 1957,
        'imdb_id': 'tt0050083'
    },
    {
        'name': 'Terkel i knibe',
        'year': 2004,
        'imdb_id': 'tt0386820'
    },
    {
        'name': 'On the Waterfront',
        'year': 1954,
        'imdb_id': 'tt0047296'
    },
    {
        'name': 'Det sjunde inseglet',
        'year': 1957,
        'imdb_id': 'tt0050976'
    },
]


@app.route('/')
def index():
    return "Movie service index"


@app.route('/movies/')
def get_movies():
    return jsonify(movies)