class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = ""

    SESSION_COOKIE_SECURE = False

    # MYSQL
    MYSQL_DATABASE_USER = ""
    MYSQL_DATABASE_PASSWORD = ""
    MYSQL_DATABASE_DB = ""
    MYSQL_DATABASE_HOST = ""

    # JWT
    JWT_SECRET_KEY = ''
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = False

    # MAIL
    MAIL_SERVER = ""
    MAIL_PORT = 465
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
