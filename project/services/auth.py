import calendar
import datetime

import jwt
from flask import abort, request

from project.config import Config
from project.services.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        # print("пароль юзера", user.password)
        # print("полученный пароль", password)
        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                print('пароли не сходятся')
                abort(400)

        data = {
            "email": user.email
            # "role": user.role
        }

        # 30 minutes for access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.ALGO)

        # 130 days for refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.ALGO)

        # print(access_token)
        # print(refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=Config.JWT_SECRET, algorithms=[Config.ALGO])
        email = data.get("email")

        return self.generate_tokens(email, None, is_refresh=True)

    def auth_required(self, func):
        def wrapper(*args, **kwargs):
            if "Authorization" not in request.headers:
                abort(401)

            data = request.headers["Authorization"]
            token = data.split('Bearer ')[-1]
            try:
                jwt.decode(token, Config.JWT_SECRET, algorithms=Config.ALGO)
                # print(jwt.decode(token, Config.JWT_SECRET, algorithms=Config.ALGO))
            except Exception as e:
                print(e)
                abort(401)
            return func(*args, **kwargs)

        return wrapper

    def admin_required(self, func):
        def wrapper(*args, **kwargs):
            if "Authorization" not in request.headers:
                abort(401)

            data = request.headers["Authorization"]
            token = data.split("Bearer ")[-1]
            role = None

            try:
                user = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.ALGO])
                role = user.get("role", "user")
            except Exception as e:
                print("JWT Decode Exception", e)
                abort(401)

            if role != "admin":
                abort(403)

            return func(*args, **kwargs)

        return wrapper
