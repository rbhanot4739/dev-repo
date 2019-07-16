import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, __file__.rsplit('.')[0]+'.sql')
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

Migrate(app, db)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    books = db.relationship('Books', backref='author', lazy='select')


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


if __name__ == '__main__':
    author1 = Authors(name='Paul Coelho')
    author2 = Authors(name='Napolean Hill')
    author3 = Authors(name='Joseph Murphy')

    book1 = Books(title='The Alchemist', author_id=1)
    book2 = Books(title='The Fifth Mountain', author_id=1)
    book3 = Books(title='Think and Grow Rich', author_id=2)
    book4 = Books(title='The Power of Subconscious Mind', author_id=3)
    book5 = Books(title='Believe in yourself', author_id=3)
    book6 = Books(title='The power of faith', author_id=3)

    db.session.add_all([author1, author2, author3, book1, book2, book3, book4, book5, book6])
    db.session.commit()



