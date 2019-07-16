from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DefaultConfig
from project.forms import AddPuppyForm, DeletePuppyForm, AddOwnerForm

app = Flask(__name__)
app.config.from_object(DefaultConfig)
# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
Migrate(app, db)

from models import Owner, Puppies


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/add", methods=['GET', 'POST'])
def add_puppy():
    form = AddPuppyForm()
    if form.validate_on_submit():
        name = form.name.data
        puppy = Puppies(name=name)
        db.session.add(puppy)
        db.session.commit()
        return redirect(url_for("list_puppies"))
    return render_template('add_puppy.html', form=form)


@app.route("/delete", methods=['GET', 'POST'])
def delete_puppy():
    form = DeletePuppyForm()
    if form.validate_on_submit():
        puppy_id = form.id.data
        puppy = Puppies.query.get(puppy_id)
        db.session.delete(puppy)
        db.session.commit()
        return redirect(url_for("list_puppies"))
    return render_template('delete_puppy.html', form=form)


@app.route("/list")
def list_puppies():
    pupps = db.session.query(Puppies).all()
    return render_template("list_puppies.html", puppies=pupps)


@app.route("/addowner", methods=['GET', 'POST'])
def add_owner():
    form = AddOwnerForm()
    if form.validate_on_submit():
        owner_name = form.owner_name.data
        puppy_name = form.puppy_name.data
        owner = Owner(name=owner_name)
        db.session.add(owner)
        db.session.commit()
        puppy = Puppies.query.filter_by(name=puppy_name).first()
        puppy.owner = owner
        db.session.commit()
        return redirect(url_for("list_puppies"))
    return render_template('add_owner.html', form=form)


if __name__ == '__main__':
    app.run()
