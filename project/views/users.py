from flask import request, abort
from flask_restx import Resource, Namespace

from project.dao.model.user import UserSchema
from project.implemented import user_service

user_ns = Namespace('/login')


@user_ns.route('/')  # /<int:uid>
class UserView(Resource):
    def get(self):
        user = user_service.get_one_by_jwt()
        res = UserSchema().dump(user)
        print(res)
        return res, 200

    def patch(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204


@user_ns.route('/<int:uid>/password')
class UserPasswordView(Resource):
    def put(self, uid):
        user = user_service.get_one(uid, calling_get=False)
        req_json = request.json

        password_now = req_json.get("password_now")
        password_new = req_json.get("password_new")

        if not user_service.compare_passwords(user.password, password_now):
            print('пароли не сходятся')
            abort(400)

        user_service.update_password(uid, password_new)
        print('пароль обновлен')

        # print(password_now)
        # print(password_new)

        return "", 204
