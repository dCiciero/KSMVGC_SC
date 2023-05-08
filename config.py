import os
basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.join(basedir, 'vgcsc/static/images/uploads')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_DATABASE_URL') #'sqlite:///' + os.path.join(basedir, 'vgcsc_sqlite.db')
    # os.environ.get('DATABASE_URL') #or \
        #'sqlite:///' + os.path.join(basedir, 'vgcsc.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_POOL_TIMEOUT = 20
    UPLOAD_FOLDER = upload_folder
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(basedir, 'cache')
    SESSION_FILE_THRESHOLD = 1000
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    APP_SETTINGS = os.getenv('APP_SETTINGS') # os.environ.get('APP_SETTINGS')
    FLASKS3_BUCKET_NAME = 'awsogcicerobucket'


class ProductionConfig(Config):
    'Production specific config'
    DEBUG = False

class StagingConfig(Config):
    'Staging specific config'
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = True
    SECRET_KEY = 'The Quick Brown Fox Jumps Over The Lazy Dog'