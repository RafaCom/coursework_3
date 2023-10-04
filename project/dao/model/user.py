from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    favorite_genre = db.Column(db.String(50))


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()


# with app.app_context():
#     db.drop_all()
#     db.create_all()
#
#     u1 = User(email="vasya@gmail.com", password="my_little_pony", name="vasya", surname='vasyanorm', favorite_genre='drama')
#     u2 = User(email="oleg@gmail.com", password="query", name="oleg", surname='olegnorm', favorite_genre='drama')
#     # u3 = User(username="oleg", password="P@ssw0rd", role="admin")
#
#     with db.session.begin():
#         db.session.add_all([u1, u2])

