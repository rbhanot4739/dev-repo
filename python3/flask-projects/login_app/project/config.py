import os


class DefaultConfig:
    SECRET_KEY = 'dummy-secret-key-for-testing'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'project', 'static',
                                 'profile_pics')
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)


class Development(DefaultConfig):
    DEBUG = True
    TESTING = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        DefaultConfig.basedir, 'db.sqlite')


class Production:
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                'mJw8V2ZetKx56MsRKRHjavi46UDgVB6tMwzZ46xmRKB1ZpWt9zqEXPi5IUedFKfbEg6y81PVd43Au0Wy')
