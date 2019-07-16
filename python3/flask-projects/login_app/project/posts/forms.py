from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, length, ValidationError
from ..models import Posts


class PostsForm(FlaskForm):
    pass


class CreatePostsForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            length(
                min=1,
                max=100,
                message="Title must between 20 and" "100 characters only",
            ),
        ],
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), length(min=1, max=1000)]
    )
    post = SubmitField("Post")

    def validate_title(self, field):
        post_title = Posts.query.filter_by(title=field.data).first()
        if post_title:
            raise ValidationError("The title already exists in the database")
