from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://flask_admin:test123@localhost/flask_apps'
db = SQLAlchemy(app)


class Marvel(db.Model):
    __tablename__ = 'Marvel_Heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    power = db.Column(db.Text())

    def __init__(self, id, name, power):
        self.id = id
        self.name = name
        self.power = power


class DC(db.Model):
    __tablename__ = 'DC_Heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    power = db.Column(db.Text())

    def __init__(self, id, name, power):
        self.id = id
        self.name = name
        self.power = power


if __name__ == '__main__':
    db.create_all()  # Creates all the tables at once
    print(db.engine)
    # DC.__table__.drop(db.engine)                           # Drops a particular table
    Marvel.__table__.create(db.engine, checkfirst=True)  # Creates a particular table
    db.drop_all()  # Drops all the tables for the existing database connection handler
