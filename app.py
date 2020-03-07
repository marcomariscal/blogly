"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'verysecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """Show 5 most recent posts."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('home.html', posts=posts)


@app.route('/users')
def users():
    """Shows all users."""

    users = User.query.all()

    return render_template('users.html', users=users)


@app.route('/users/new')
def add_user_page():
    """Show add new user form."""

    return render_template('new-user-form.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """Get new user form inputs to create new user."""
    first = request.form.get('first')
    last = request.form.get('last', 0)
    image = request.form.get('image', 0)

    user = User(first_name=first, last_name=last, image_url=image)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_page(user_id):
    """User detail page."""

    user = User.query.get(user_id)

    return render_template('user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):

    user = User.query.get(user_id)

    return render_template('edit-user-form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):

    first = request.form.get('first')
    last = request.form.get('last', 0)
    image = request.form.get('image', 0)

    user = User.query.get(user_id)
    user.first_name = first
    user.last_name = last
    user.image_url = image

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):

    user = User.query.get(1)
    db.session.delete(user)

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Shows new post form."""

    user = User.query.get(user_id)

    return render_template('new-post-form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Get form information to create new post."""

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'] or None,
        user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Handle form submission for delete post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
