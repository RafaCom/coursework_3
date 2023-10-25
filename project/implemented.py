from project.dao.director import DirectorDAO
from project.dao.genre import GenreDAO
from project.dao.movie import MovieDAO
from project.dao.user import UserDAO
from project.dao.user_movie_association import UserMovieAssociationDAO
from project.services.auth import AuthService
from project.services.director import DirectorService
from project.services.genre import GenreService
from project.services.movie import MovieService
from project.services.user import UserService
from project.services.user_movie_association import UserMovieAssociationService

from project.db.setup_db import db

movie_dao = MovieDAO(db.session)
user_dao = UserDAO(db.session)
user_movie_association = UserMovieAssociationDAO(db.session)
genre_dao = GenreDAO(db.session)
director_dao = DirectorDAO(db.session)

movie_service = MovieService(movie_dao)
user_service = UserService(user_dao)
auth_service = AuthService(user_service)
user_movie_association_service = UserMovieAssociationService(user_movie_association)
genre_service = GenreService(genre_dao)
director_service = DirectorService(director_dao)
