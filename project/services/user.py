import base64
import hashlib
import hmac

import jwt
from flask import abort, request

from project.config import Config
from project.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    @staticmethod
    def __get_hash(password: str) -> str:
        hash_digest = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            salt=Config.PDW_HASH_SALT,
            iterations=Config.PDW_HASH_ITERATIONS,
            password=password.encode('utf-8'),  # Convert the password to bytes
        )
        return base64.b64encode(hash_digest).decode('utf-8')

    def compare_passwords(self, password_hash, other_password):
        # decoded_digest = base64.b64decode(password_hash)

        hash_digest = self.__get_hash(other_password)
        # print("полученный пароль в виде хэша", hash_digest)

        return hmac.compare_digest(password_hash, hash_digest)

    def __get_uid_by_jwt(self):
        if "Cookie" not in request.headers:
            print('тут')
            abort(401)

        data = request.headers["Cookie"]
        token = data.split("AccessToken=")[-1]
        ready_token = token.split(";")[0]
        print(ready_token)

        try:
            user = jwt.decode(ready_token, Config.JWT_SECRET, algorithms=[Config.ALGO])
            email_jwt = user.get("email")
            user_by_email = self.get_by_username(email_jwt)
            uid = user_by_email.id

        except Exception as e:
            print('тут')
            print("JWT Decode Exception", e)
            abort(401)

        if uid is None:
            abort(404)

        return uid

    def get_one_by_jwt(self):
        uid = self.__get_uid_by_jwt()
        user = self.get_one(uid)
        return user

    def get_one(self, uid, calling_get=True):
        user = self.dao.get_one(uid)
        if calling_get:
            user.password = str(user.password)
        return user

    def get_by_username(self, email):
        return self.dao.get_by_email(email)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        data['password'] = self.__get_hash(data['password'])
        return self.dao.create(data)

    def update(self, data):
        print(data)
        # if "password" in data:
        #     data['password'] = self.get_hash(data['password'])
        self.dao.update(data)

    def update_password(self, uid, new_password):
        new_password = self.__get_hash(new_password)
        self.dao.update_password(uid, new_password)

    def delete(self, mid):
        self.dao.delete(mid)

        