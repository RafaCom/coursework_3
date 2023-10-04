from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer

from project.setup_db import db


class Director(db.Model):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
