from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class MainForm(FlaskForm):
    hostname = StringField(label='Hostname', validators=[DataRequired()])
    database_type = SelectField(label='Database Type', choices=[('mysql', 'MySQL'), ('postgres', 'PostgresSQL')])
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class TasksForm(FlaskForm):
    ports = SelectField('Select port', coerce=int)
    submit = SubmitField('Submit')
