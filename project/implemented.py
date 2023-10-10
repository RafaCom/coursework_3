from project.dao.movie import MovieDAO
from project.dao.user import UserDAO
from project.services.auth import AuthService
from project.services.movie import MovieService
from project.services.user import UserService

from setup_db import db

movie_dao = MovieDAO(db.session)
user_dao = UserDAO(db.session)

movie_service = MovieService(movie_dao)
user_service = UserService(user_dao)
auth_service = AuthService(user_service)

