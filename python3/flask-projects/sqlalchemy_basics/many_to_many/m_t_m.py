import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, __file__.split(".")[0])}.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
Migrate(app, db)

link = db.Table('link', db.Column('actor.id', db.Integer, db.ForeignKey('actor.id')),
                db.Column('movie.id', db.Integer, db.ForeignKey('movie.id')))


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    # movies_done = db.relationship('Movie', secondary='link', backref='actor', lazy='dynamic')
    movies_done = db.relationship('Movie', secondary='link', backref=db.backref('actor', lazy='dynamic'),
                                  lazy='dynamic')


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


if __name__ == '__main__':
    a1 = Actor(name='Keanu Reevs')
    a2 = Actor(name='Tom Cruise')
    a3 = Actor(name='Jeremy Renner')
    m1 = Movie(name='John Wick')
    m2 = Movie(name='Speed')
    m3 = Movie(name='Matrix')
    m4 = Movie('Vanilla Sky')
    m5 = Movie(name='Mission Impossible')
    m6 = Movie(name='The Town')
