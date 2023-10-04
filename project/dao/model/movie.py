from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup_db import db


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id"), nullable=False)
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("director.id"), nullable=False)
    director = relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

