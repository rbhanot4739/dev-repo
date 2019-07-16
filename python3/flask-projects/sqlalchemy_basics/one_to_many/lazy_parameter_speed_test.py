import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from random import randint
from time import time

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, __file__.rsplit('.')[0] + '.sql')
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

Migrate(app, db)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    books = db.relationship('Books', backref='author', lazy='select')  # Time :  0.07908868789672852
    # books = db.relationship('Books', backref='author', lazy='dynamic')  # Time :  0.07604742050170898
    # books = db.relationship('Books', backref='author', lazy='joined')  # Time :  1.4440464973449707
    # books = db.relationship('Books', backref='author', lazy='subquery')  # Time : 1.467285394668579


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


def populate_authors_table():
    for i in range(10000):
        author = Authors(name='User' + str(i))
        db.session.add(author)
    db.session.commit()


def populate_books_table():
    for i in range(90000):
        b = Books(title='Book' + str(i), author_id=randint(1, 9999))
        db.session.add(b)
    db.session.commit()


if __name__ == '__main__':
    # populate_authors_table()
    # populate_books_table()

    start = time()
    auths = Authors.query.all()
    print(time() - start)
