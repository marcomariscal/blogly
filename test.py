from unittest import TestCase
from app import app
from models import db, User, Post


class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        db.drop_all()
        db.create_all()

        # create user to test
        user = User(first_name="sponge", last_name="bob")
        db.session.add(user)

        # create post to test
        post = Post(title="first post",
                    content="first bit of content", user_id=1)

        db.session.add(post)
        db.session.commit()

    def test_users_page(self):

        response = self.client.get('/users')

        self.assertIn(b'sponge bob', response.data)

    def test_edit_user_page(self):

        response = self.client.get('users/1/edit')
        self.assertIn('200 OK', response.status)

    def test_delete_user(self):

        self.client.post('/users/1/delete')

        self.assertIsNone(User.query.get(1))

    def test_add_user(self):

        new_user = User(first_name='tommy', last_name="bahama")
        db.session.add(new_user)
        db.session.commit()

        self.assertIsNotNone(User.query.filter_by(first_name='tommy'))

    def test_add_post(self):

        new_post = Post(title='nice post title',
                        content="some post content", user_id=1)
        db.session.add(new_post)
        db.session.commit()

        self.assertIsNotNone(Post.query.filter_by(
            title='nice post title', content='some post content'))

    def test_delete_post(self):

        self.client.post('/posts/1/delete')

        self.assertIsNone(Post.query.get(1))
