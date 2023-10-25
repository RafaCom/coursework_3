from flask import request
from flask_restx import Namespace, Resource

from project.implemented import user_service, auth_service

auth_ns = Namespace("/auth")


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        req_json = request.json

        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None is [email, password]:
            return "", 400

        user_service.create(req_json), 201


@auth_ns.route('/login/')
class AuthLoginView(Resource):
    def post(self):
        req_json = request.json

        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None is [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self):
        req_json = request.json
        token = req_json.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
