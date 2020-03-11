"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
def user_add_page():
    """Show add new user form."""

    return render_template('user-new-form.html')


@app.route('/users/new', methods=['POST'])
def user_add():
    """Get new user form inputs to create new user."""
    first = request.form.get('first')
    last = request.form.get('last', 0)
    image = request.form.get('image', 0)

    user = User(first_name=first, last_name=last, image_url=image)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """User detail page."""

    user = User.query.get(user_id)

    return render_template('user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def user_edit_page(user_id):

    user = User.query.get(user_id)

    return render_template('user-edit-form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_edit(user_id):

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
def user_delete(user_id):

    user = User.query.get(1)
    db.session.delete(user)

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def post_add_page(user_id):
    """Shows new post form."""

    user = User.query.get(user_id)

    tags = Tag.query.all()

    return render_template('post-new-form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_add(user_id):
    """Get form information to create new post."""

    new_post = Post(
        title=request.form['title'],
        content=request.form['content'] or None,
        user_id=user_id)

    tags = request.form.getlist('checkboxes')

    tags = Tag.query.filter(Tag.name.in_(tags))

    new_post.tags.extend(tags)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def post_page(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def post_edit_page(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post-edit-form.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit(post_id):

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = []

    tags = request.form.getlist('checkboxes')

    tags = Tag.query.filter(Tag.name.in_(tags))

    post.tags.extend(tags)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def post_delete(post_id):
    """Handle form submission for delete post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.errorhandler(404)
def error_page(e):
    return render_template('error.html'), 404


@app.route('/tags', methods=["GET"])
def tag_show_all():
    """Show all tags."""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>', methods=["GET"])
def tag_detail_page(tag_id):
    """Show tag detail page."""

    tag = Tag.query.get(tag_id)

    return render_template('tag.html', tag=tag)


@app.route('/tags/new', methods=["GET"])
def tag_new_page():
    """Create new tag form."""

    return render_template('tag-new-form.html')


@app.route('/tags/new', methods=["POST"])
def tag_new():
    """Create new tag using form inputs."""

    name = request.form["name"]

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def tag_edit_page(tag_id):
    """Edit tag detail form."""

    tag = Tag.query.get(tag_id)

    return render_template('tag-edit-form.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tag_edit(tag_id):
    """Edit tag detail form."""

    tag = Tag.query.get(tag_id)

    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tag_delete(tag_id):
    """Delete tag."""

    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
