from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from .forms import CreatePostsForm
from .. import db
from ..models import Posts

posts = Blueprint('posts', __name__)


@posts.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostsForm()
    if form.validate_on_submit():
        user = current_user.id
        post = Posts(
            title=form.title.data,
            description=form.description.data,
            author_id=user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show_all_posts'))
    return render_template('posts/create_update_post.html', form=form,
                           title='Create Post')


@posts.route("/post/int: <post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author == current_user:
        form = CreatePostsForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.description = form.description.data
            post.creation_date = datetime.utcnow()
            db.session.commit()
            return redirect(url_for("posts.show_post", post_id=post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.description.data = post.description
        return render_template('posts/create_update_post.html', form=form)
    else:
        return redirect(url_for("posts.show_all_posts"))


@posts.route("/show_posts")
def show_all_posts():
    page_num = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.creation_date.desc()).paginate(
        page=page_num, per_page=3)
    return render_template("posts/show_all_posts.html", posts=posts,
                           page_num=page_num)


@posts.route("/post/int: <post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template("posts/show_post.html", post=post)


@posts.route("/post/int: <post_id>/delete", methods=['GET', 'POST'])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.show_all_posts'))
