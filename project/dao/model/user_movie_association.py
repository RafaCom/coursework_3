from marshmallow import Schema, fields

from project.dao.model.movie import Movie
from project.dao.model.user import User
from project.db.setup_db import db


class UserMovieAssociation(db.Model):
    __tablename__ = "user_movie_association"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    movie = db.relationship("Movie")


class UserMovieAssociationSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    movie_id = fields.Int()
