from sqlalchemy.orm import aliased

from project.dao.model.movie import Movie
from project.dao.model.user import User
from project.dao.model.user_movie_association import UserMovieAssociation


class UserMovieAssociationDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid, mid):
        # print(Movie.query.join(UserMovieAssociation, (UserMovieAssociation.movie_id == mid)).one())
        return Movie.query.join(UserMovieAssociation, (UserMovieAssociation.movie_id == mid)).one()

    def get_all(self, uid):
        # print(self.session.query(UserMovieAssociation, Movie).join(Movie).filter(UserMovieAssociation.user_id == uid).all())
        return (
            self.session.query(UserMovieAssociation, Movie).join(Movie).filter(UserMovieAssociation.user_id == uid).all()
        )

    def create(self, data):
        line = UserMovieAssociation(**data)
        self.session.add(line)
        self.session.commit()
        self.session.close()

    def delete(self, lid):
        line = self.session.query(UserMovieAssociation).get(lid)
        self.session.delete(line)
        self.session.commit()
        self.session.close()
        