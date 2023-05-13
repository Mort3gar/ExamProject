
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:PASSWORD@localhost/NAME"



class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secterpassword'