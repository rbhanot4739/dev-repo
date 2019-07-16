from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddPuppyForm(FlaskForm):
    name = StringField('Enter the Puppy Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeletePuppyForm(FlaskForm):
    id = IntegerField('Enter the Puppy id', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddOwnerForm(FlaskForm):
    owner_name = StringField('Owner Name', validators=[DataRequired()])
    puppy_name = StringField('Puppy Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
