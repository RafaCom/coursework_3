from project.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        self.session.close()

        return user

    def update(self, data):
        user = self.get_one(data.get("id"))
        if "email" in data:
            user.email = data.get("email")
        # if "password" in data:
        #     user.password = data.get("password")
        if "name" in data:
            user.name = data.get("name")
        if "surname" in data:
            user.surname = data.get("surname")
        if "favorite_genre_id" in data:
            user.favorite_genre = data.get("favorite_genre_id")

        print(user.password)
        self.session.add(user)
        self.session.commit()
        self.session.close()

    def update_password(self, uid, new_password):
        user = self.get_one(uid)
        user.password = new_password
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
        self.session.close()

