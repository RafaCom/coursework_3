from project.dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        movie = self.dao.get_one(mid)
        return movie

    def get_all(self, filters):
        return self.dao.get_all(filters)

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        self.dao.update(data)

    def delete(self, mid):
        self.dao.delete(mid)

