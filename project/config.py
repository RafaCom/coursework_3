class Config(object):
    DEBUG = True
    ALGO = 'HS256'
    JWT_SECRET = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # sqlite:///:memory:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PDW_HASH_SALT = b'secret_here'
    PDW_HASH_ITERATIONS = 100_000
    RESTX_JSON = {'ensure_ascii': False, 'indent': 4}

