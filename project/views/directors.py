from flask_restx import Namespace, Resource

from project.dao.model.director import DirectorSchema
from project.implemented import director_service


director_ns = Namespace("directors")


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = director_service.get_all()
        res = DirectorSchema(many=True).dump(all_directors)
        return res, 200


@director_ns.route('/<int:did>/')
class DirectorView(Resource):
    def get(self, did):
        director = director_service.get_one(did)
        res = DirectorSchema().dump(director)
        return res, 200
