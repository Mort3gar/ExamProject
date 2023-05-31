
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Djkmcrfz50!@localhost/temp3"



class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secterpassword'