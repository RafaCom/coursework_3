import json

from flask import Flask, render_template

from flask_restx import Api

from project.config import Config
from project.dao.model.user import User
from project.dao.model.director import Director
from project.dao.model.genre import Genre
from project.dao.model.movie import Movie
from project.dao.model.user_movie_association import UserMovieAssociation
from project.views.auth import auth_ns
from project.views.directors import director_ns
from project.views.genres import genre_ns

from project.views.movies import movie_ns
from project.views.user_movie_associations import favorites_ns
from project.views.users import user_ns
from project.db.setup_db import db


def create_app(config_object):
    application = Flask(__name__)
    application.config.from_object(config_object)

    @application.route('/')
    def index():
        return render_template('index.html')

    register_extensions(application)

    return application


def register_extensions(application):
    api = Api(title="Flask Course Project 3", doc="/docs")
    api.init_app(application)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(favorites_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)

    db.init_app(application)
    # create_data(application, db)
    # load_data_from_json('/Users/rafaelsirinan/Desktop/Python Projects/coursework_3/data_for_db.json', application, db)


def create_data(application, database):
    with application.app_context():
        database.drop_all()
        database.create_all()

        u1 = User(email="vasya@gmail.com", password="my_little_pony", name="vasya", surname='vasyanorm', favorite_genre_id=1)
        u2 = User(email="oleg@gmail.com", password="query", name="oleg", surname='olegnorm', favorite_genre_id=4)
        u3 = User(email="katy@gmail.com", password="query___", name="katy", surname='katynorm', favorite_genre_id=3)

        # g1 = Genre(name='drama')
        # g2 = Genre(name='comedy')
        # g3 = Genre(name='fantastic')
        # g4 = Genre(name='action movie')

        f1 = UserMovieAssociation(user_id=1, movie_id=19)
        f2 = UserMovieAssociation(user_id=4, movie_id=12)
        f3 = UserMovieAssociation(user_id=4, movie_id=6)
        f4 = UserMovieAssociation(user_id=3, movie_id=14)
        f5 = UserMovieAssociation(user_id=2, movie_id=10)

        database.session.add_all([u1, u2, u3, f1, f2, f3, f4, f5])
        database.session.commit()


def load_data_from_json(json_file_path, application, database):
    with application.app_context():
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
    app.run(port=25000, debug=True)  # host='0.0.0.0',


""" Написать тесты
    Проверить, правильно ли я понял и создал таблицу "многие ко многим"
    
    
    так как я добавил в импортах для моделей project.setup_db, 
    не запускается приложение, зато работают тесты (но там своя ошибка)
    
    РЕШЕНИЕ --- для файла с созданием базы данных создать отдельный модуль и туда его поместить 
 """

"""
frontend
не находит ------ /manifest.json HTTP/1.1" 404 -
как связать с бэкендом???




!!!!! ГОТОВО, НО МНОГО НЕДОРАБОТОК ИЗ-ЗА фронта !!!!!

"""
