import hashlib
import hmac

from project.config import Config
from project.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, email):
        return self.dao.get_by_email(email)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        data['password'] = self.get_hash(data['password'])
        return self.dao.create(data)

    def update(self, data):
        data['password'] = self.get_hash(data['password'])
        self.dao.update(data)

    def delete(self, mid):
        self.dao.delete(mid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            Config.PDW_HASH_SALT,
            Config.PDW_HASH_ITERATIONS
        )
        # print(hash_digest)
        return hash_digest

    def compare_passwords(self, password_hash, other_password):
        # decoded_digest = base64.b64decode(password_hash)

        hash_digest = self.get_hash(other_password)
        # print("полученный пароль в виде хэша", hash_digest)

        return hmac.compare_digest(password_hash, hash_digest)

        