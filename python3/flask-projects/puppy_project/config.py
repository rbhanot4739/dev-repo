from os import environ, path


class DefaultConfig:
    DEBUG = True
    try:
        SECRET_KEY = environ['SECRET_KEY']
    except KeyError:
        SECRET_KEY = 'really-weak-secret-key'
        print(
            'Using 99_dummy secret key for Dev, Consider using strong key in Production !!.'
            'Please set SECRET_KEY env variable and export it !!')
        # sys.exit('SECRET KEY Missing !! Please set SECRET_KEY env variable and export it.')

    basedir = path.abspath(path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'puppies.sql')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
