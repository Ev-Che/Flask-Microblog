import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdkjfhaswqrjwre'

    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or
                               'sqlite:///' + os.path.join(BASEDIR,
                                                           'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT' or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ev.che2001@gmail.com']

    POSTS_PER_PAGE = 10

    LANGUAGES = ['en', 'de', 'ru']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
