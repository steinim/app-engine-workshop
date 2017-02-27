import logging
import json
import os

from google.appengine.api import users, urlfetch, modules
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index page 4'


@app.route('/hello-world/')
def hello_world():
    current_user = users.get_current_user()
    return "Hello {}. You are running your app on {}.".format(current_user, os.environ['SERVER_NAME']) 


@app.route('/test-static/')
def test_static():
    return '<img src="/static/img/img.png" />'


@app.route('/test-logging')
def test_logging():
    print("This is a print to stdout")
    logging.debug('This is just a debug message')
    logging.info('Info message')
    logging.warning('Someone has done something weird here...')
    logging.error('Now something went terribly wrong')
    logging.critical('Oh, shit!')
    logging.exception('An exception was thrown and we are logging it')

    return "Testing logging"


@app.route('/user/')
def check_user():
    current_user = users.get_current_user()

    if current_user is not None:
        user_nickname = current_user.nickname()

        return "Currently logged in as: {}<br />{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>{}<br/>Is Admin: {}<br/><a href='{}'>Logout</a>".format(
            user_nickname,
            current_user,
            current_user.email(),
            current_user.auth_domain(),
            current_user.federated_identity(),
            current_user.federated_provider(),
            current_user.user_id(),
            users.is_current_user_admin(),
            users.create_logout_url('/user')
        )
    else:
        return "Not logged in<br/><a href='{}'>Login</a>".format(users.create_login_url('/user'))


@app.route('/user-area/')
def user_area():
    current_user = users.get_current_user()
    is_admin = users.is_current_user_admin()

    return "Hello, {}.<br/>Is admin: {}".format(current_user, is_admin)


@app.route('/secure-area/')
def secure_area():
    current_user = users.get_current_user()
    is_admin = users.is_current_user_admin(),

    return "Hello, {}.<br/>Is admin: {}".format(current_user, is_admin)


def format_movie(movie):
    return '<a href="http://www.imdb.com/title/{}">{} ({})</a><br />'.format(movie['imdb_id'],
                                                                             movie['name'],
                                                                             movie['year'])


@app.route('/get-movies/')
def get_movies():
    movie_service_url = modules.get_hostname(module='movie')
    movie_movies_url = 'http://' + movie_service_url + '/movies/'

    response = ""

    try:
        result = urlfetch.fetch(movie_movies_url)

        if result.status_code == 200:
            movies = json.loads(result.content)

            response += 'Got {} movies from {}'.format(len(movies), movie_movies_url)
            response += '<br/>-----<br />'
            response += ''.join([format_movie(movie) for movie in movies])
        else:
            response += 'Could not fetch movies from {}.<br/>'.format(movie_movies_url)
            response += 'Got response code {}.'.format(result.status_code)

    except Exception as e:
        response += 'Could not fetch movies from {}'.format(movie_movies_url)
        response += '<br/>'
        response += str(e)


    return response
