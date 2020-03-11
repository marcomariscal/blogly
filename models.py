from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://i.stack.imgur.com/34AD2.jpg'


"""Models for Blogly."""


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)

    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", backref='user',
                            cascade='all, delete-orphan')


class Post(db.Model):
    """Post. A User's post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text,
                      nullable=False)

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag',
                           secondary='posts_tags',
                           backref='posts')

    @property
    def nice_date(self):
        """Return nicely formatted date."""

        return self.created_at.strftime("%m/%d/%y")


class PostTag(db.Model):
    """Post and tag association."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """A tag that can be associated with a post."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False, unique=True)


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
