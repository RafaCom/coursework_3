from flask import request
from flask_restx import Namespace, Resource

from project.dao.model.user_movie_association import UserMovieAssociationSchema
from project.implemented import user_movie_association_service, auth_service

favorites_ns = Namespace('/favorites/movies')


@favorites_ns.route('/')
class UserMovieAssociationView(Resource):
    # @auth_service.auth_required
    def get(self):
        favorites_movies = user_movie_association_service.get_all()
        # res = UserMovieAssociationSchema(many=True).dump(favorites_movies)
        # print(favorites_movies)
        return favorites_movies

    def post(self):
        req_json = request.json
        user_movie_association_service.create(req_json)
        return "", 201


@favorites_ns.route('/<int:mid>')
class UserMovieAssociationView(Resource):
    def get(self, mid):
        favorite = user_movie_association_service.get_one(mid)
        return favorite

    def delete(self, lid):
        user_movie_association_service.delete(lid)
        return "", 204
