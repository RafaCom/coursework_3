from project.dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self, filters):
        movies = self.session.query(Movie)
        if "status" in filters and filters['status'] is not None:
            movies = movies.order_by(Movie.year.desc())

        if "page" in filters and filters['page'] is not None:
            per_page = 12
            offset = (filters['page'] - 1) * per_page
            movies = movies.offset(offset).limit(12)

        return movies.all()
        # return self.session.query(Movie).all()

    def pagination_by_12(self, offset):
        return self.session.query(Movie).offset(offset).limit(12).all()

    def sorting_by_year(self):
        return self.session.query(Movie).order_by(Movie.year.desc()).all()

    # def pagination_and_sorting(self, status,):

    def create(self, data):
        movie = Movie(**data)
        self.session.add(movie)
        self.session.commit()
        self.session.close()

        return movie

    def update(self, data):
        movie = self.get_one(data.get("id"))
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")

        self.session.add(movie)
        self.session.commit()
        self.session.close()

    def delete(self, mid):
        movie = self.get_one(mid)
        self.session.delete(movie)
        self.session.commit()
        self.session.close()
