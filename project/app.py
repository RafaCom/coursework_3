import json

from flask import Flask

from flask_restx import Api

from config import Config
from dao.model.user import User
from project.dao.model.director import Director
from project.dao.model.genre import Genre
from project.dao.model.movie import Movie
from project.views.auth import auth_ns

from project.views.movies import movie_ns
from setup_db import db


def create_app(config_object):
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    return application


def register_extensions(application):
    db.init_app(application)
    create_data(application, db)
    load_data_from_json('/Users/rafaelsirinan/Desktop/Python Projects/coursework_3/data_for_db.json', application, db)
    api = Api(application)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    # api.add_namespace(director_ns)
    # api.add_namespace(genre_ns)
    # api.add_namespace(user_ns)


def create_data(application, database):
    with application.app_context():
        database.drop_all()
        database.create_all()

        u1 = User(email="vasya@gmail.com", password="my_little_pony", name="vasya", surname='vasyanorm', favorite_genre='drama')
        u2 = User(email="oleg@gmail.com", password="query", name="oleg", surname='olegnorm', favorite_genre='drama')
        u3 = User(email="katy@gmail.com", password="query___", name="katy", surname='katynorm', favorite_genre='comedy')

        with database.session.begin():
            database.session.add_all([u1, u2, u3])


def load_data_from_json(json_file_path, application, database):
    with application.app_context():
        database.drop_all()
        database.create_all()

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            for item in data["movies"]:
                movie = Movie(
                    id=item['pk'],
                    title=item['title'],
                    description=item['description'],
                    trailer=item['trailer'],
                    year=item['year'],
                    rating=item['rating'],
                    genre_id=item['genre_id'],
                    director_id=item['director_id']
                )
                database.session.add(movie)
            database.session.commit()

            for item in data["directors"]:
                director = Director(
                    id=item['pk'],
                    name=item['name']
                )
                database.session.add(director)
            database.session.commit()

            for item in data["genres"]:
                genre = Genre(
                    id=item['pk'],
                    name=item['name']
                )
                database.session.add(genre)
            database.session.commit()


app = create_app(Config())
app.debug = True


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
