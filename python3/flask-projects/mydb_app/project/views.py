from flask import redirect, render_template, session, url_for

from project import app
from project.db_mgmt_wrapper import show_mysql_running_instances, Postgres, Mysql
from project.forms import MainForm, TasksForm

database_params = {
    'mysql': (Mysql, 'root'),
    'postgres': (Postgres, 'postgres')
}


@app.route("/", methods=['GET', 'POST'])
def home():
    form = MainForm()
    if form.validate_on_submit():
        session['hostname'] = form.hostname.data
        username = form.username.data
        password = form.password.data
        session['database_type'] = form.database_type.data
        session['resp'] = show_mysql_running_instances(session['hostname'], username, password,
                                                       session['database_type'])
        return redirect(url_for("tasks"))
    return render_template("home.html", title="Home", form=form)


@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    form = TasksForm()
    if session:
        if session['resp'][-1] != 'Error':
            ports = [(int(i), i) for i in session['resp'][0]]
    form.ports.choices = ports
    if form.validate_on_submit():
        port = form.ports.data
        dbclass, user = database_params[session['database_type']]
        obj = dbclass(session['hostname'], port, user, 'TowerMyDB', session['database_type'].lower())
        return render_template("operations.html", obj=obj)
    return render_template("tasks.html", form=form)
