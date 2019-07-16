import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Development

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

# login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message = 'Please login to access this page !'
login_manager.login_message_category = 'warning'
login_manager.refresh_view = 'user.login'
login_manager.needs_refresh_message = 'Please login again to access this page'
login_manager.needs_refresh_message_category = 'info'

# application logging
if app.debug:  # for produciton this should be if not app.debug
    if not os.path.exists("logs"):
        os.mkdir("logs")
    log_handler = RotatingFileHandler("logs/app-logs", maxBytes=10240,
                                      backupCount=5)
    log_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    log_handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)

from .core.views import core
from .user.views import user
from .posts.views import posts
from .models import db, User, Posts
from . import errors

app.register_blueprint(core)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(posts, url_prefix='/posts')


@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Posts': Posts}
