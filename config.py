class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "DFGs34fdvgss#$dsfd%EF#3245SD%#%E^%$^&$#S@#TY#Y&"

    SESSION_COOKIE_SECURE = True

    # MYSQL
    MYSQL_DATABASE_USER = "pi"
    MYSQL_DATABASE_PASSWORD = "Ev12321"
    MYSQL_DATABASE_DB = "Kamil"
    MYSQL_DATABASE_HOST = "192.168.0.200"

    # JWT
    JWT_SECRET_KEY = '@df34FD%d^$W#%s#dsY$'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = False

    # MAIL
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "kamyrdol32test@gmail.com"
    MAIL_PASSWORD = "iqvfqchwmxycqdbk"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "kamyrdol32test@gmail.com"
    MAIL_PASSWORD = "iqvfqchwmxycqdbk"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "kamyrdol32test@gmail.com"
    MAIL_PASSWORD = "iqvfqchwmxycqdbk"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
