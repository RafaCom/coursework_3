import jwt
from flask import request, abort

from project import implemented
from project.config import Config
from project.dao.model.movie import MovieSchema
from project.dao.user_movie_association import UserMovieAssociationDAO


class UserMovieAssociationService:
    def __init__(self, dao: UserMovieAssociationDAO):
        self.dao = dao

    @staticmethod
    def __get_uid_by_jwt():
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            user = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.ALGO])
            email_jwt = user.get("email")
            user_by_email = implemented.user_service.get_by_username(email_jwt)
            uid = user_by_email.id

        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        if uid is None:
            abort(404)

        return uid

    # def get_one(self, mid):
    #     uid = self.__get_uid_by_jwt()
    #     favorite = self.dao.get_one(uid, mid)
    #     res = MovieSchema().dump(favorite)
    #     print(res)
    #     return res

    def get_all(self):
        uid = self.__get_uid_by_jwt()
        favorite_movies = self.dao.get_all(uid)
        ready_favorite_movies = []
        for movie in favorite_movies:
            ready_favorite_movies.append(movie[-1])
        # print(ready_favorite_movies)
        res = MovieSchema(many=True).dump(ready_favorite_movies)
        # print(res)
        return res

    def create(self, data):
        self.dao.create(data)

    def delete(self, lid):
        self.dao.delete(lid)
