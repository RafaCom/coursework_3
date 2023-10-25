from flask import request
from flask_restx import Resource, Namespace

from project.dao.model.movie import MovieSchema
from project.implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        page = request.args.get('page', type=int)
        status = request.args.get('status')

        filters = {
            "page": page,
            "status": status
        }
        # print(filters)
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:mid>/')
class MovieView(Resource):
    def get(self, mid):
        movie = movie_service.get_one(mid)
        res = MovieSchema().dump(movie)  # проблема чтения id в frontend
        print(res)
        return res, 200

    def put(self, mid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = mid
        movie_service.update(req_json)
        return "", 204

    def delete(self, mid):
        movie_service.delete(mid)
        return "", 204
