from flask_restx import Namespace, Resource

from project.dao.model.genre import GenreSchema
from project.implemented import genre_service


genre_ns = Namespace("genres")


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = genre_service.get_all()
        res = GenreSchema(many=True).dump(all_genres)
        return res, 200


@genre_ns.route('/<int:gid>/')
class GenreView(Resource):
    def get(self, gid):
        genre = genre_service.get_one(gid)
        res = GenreSchema().dump(genre)
        return res, 200
