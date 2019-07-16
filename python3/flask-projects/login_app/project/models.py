from flask_login import UserMixin
from itsdangerous import URLSafeSerializer
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from hashlib import md5

from . import app, db, login_manager

my_serializer = URLSafeSerializer(app.config['SECRET_KEY'])


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(40), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    alternate_id = db.Column(db.String(100))
    about_me = db.Column(db.String(200))
    profile_pic = db.Column(db.String(64),
                            default='0f2d25df523b8a036a54bfe15148f2c6.jpg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Posts', backref='author', lazy=True)

    def get_id(self):
        # return str(self.id)
        return str(self.alternate_id)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.alternate_id = my_serializer.dumps(
            self.username + self.password_hash)

    def verify_password(self, password):
        if check_password_hash(self.password_hash, password):
            return "True"

    def set_avatar(self, size):
        digest = md5(self.username.encode()).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(1500))
    creation_date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, author_id):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.creation_date = datetime.utcnow()


@login_manager.user_loader
def load_user(uid):
    # return User.query.get(int(uid))
    return User.query.filter_by(alternate_id=uid).first()
