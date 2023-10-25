from unittest.mock import MagicMock

import pytest

from project.dao.model.user import User
from project.dao.user import UserDAO
from project.services.user import UserService


@pytest.fixture()
def user_dao():
    user_dao = UserDAO(None)

    rafael = User(id=1, email="rafael@gmail.com", password="rafacom", name="rafael", surname='Shirinyan', favorite_genre_id=1)
    rose = User(id=2, email="rose@gmail.com", password="rosetitanic", name="rose", surname='Rosyan', favorite_genre_id=3)
    albina = User(id=3, email="albina@gmail.com", password="albinos", name="albina", surname='Shir', favorite_genre_id=2)
    user = User(id=4, email="vasya@gmail.com", password="my_little_pony", name="vasya", surname='vasyanorm', favorite_genre_id=1)

    user_dao.get_one = MagicMock(return_value=rafael)
    user_dao.get_all = MagicMock(return_value=[rafael, rose, albina])
    user_dao.create = MagicMock(return_value=user)
    user_dao.delete = MagicMock()
    user_dao.update = MagicMock()

    return user_dao


class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self, user_dao):
        self.user_service = UserService(dao=user_dao)

    def test_get_one(self):
        user = self.user_service.get_one(1)
        assert user is not None
        assert user.id is not None
        assert user.id == 1

    def test_get_all(self):
        users = self.user_service.get_all()
        assert len(users) > 0
        assert len(users) == users[-1].id

    def test_create(self):
        user_d = {
            "id": 4,
            "email": "vasya@gmail.com",
            "password": "my_little_pony",
            "name": "vasya",
            "surname": 'vasyanorm',
            "favorite_genre_id": 1
        }
        user = self.user_service.create(user_d)
        assert user.id is not None
        assert user.email == "vasya@gmail.com"

    def test_update(self):
        user_d = {
            "email": "vas@gmail.com",
            "password": "my_little_pony",
            "name": "vas",
            "surname": 'vasyanorm',
            "favorite_genre_id": 1
        }
        user = self.user_service.update(user_d)

