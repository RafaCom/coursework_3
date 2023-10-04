from flask import Flask

# from flask_restx import Api

from config import Config
from dao.model.user import User
# from project.dao.model.user import User
from setup_db import db


# from views.auth import auth_ns
# from views.directors import director_ns
# from views.genres import genre_ns
# from views.movies import movie_ns
# from views.users import user_ns


def create_app(config_object):
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    return application


def register_extensions(application):
    db.init_app(application)
    create_data(application, db)
    # api = Api(application)
    # api.add_namespace(director_ns)
    # api.add_namespace(genre_ns)
    # api.add_namespace(movie_ns)
    # api.add_namespace(user_ns)
    # api.add_namespace(auth_ns)


# class User(db.Model):
#     __tablename__ = 'user'
#
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     name = db.Column(db.String(50))
#     surname = db.Column(db.String(50))
#     favorite_genre = db.Column(db.String(50))


def create_data(application, database):
    with application.app_context():
        database.drop_all()
        database.create_all()

        u1 = User(email="vasya@gmail.com", password="my_little_pony", name="vasya", surname='vasyanorm', favorite_genre='drama')
        u2 = User(email="oleg@gmail.com", password="query", name="oleg", surname='olegnorm', favorite_genre='drama')
        u3 = User(email="katy@gmail.com", password="query___", name="katy", surname='katynorm', favorite_genre='comedy')

        with database.session.begin():
            database.session.add_all([u1, u2, u3])


app = create_app(Config())
app.debug = True


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
