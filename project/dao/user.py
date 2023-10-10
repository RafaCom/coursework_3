from project.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

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
        user.email = data.get("email")
        user.password = data.get("password")
        user.name = data.get("name")
        user.surname = data.get("surname")
        user.favorite_genre = data.get("favorite_genre")

        self.session.add(user)
        self.session.commit()
        self.session.close()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()
        self.session.close()

