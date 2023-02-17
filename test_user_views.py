""" User_view_tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py
import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_user(self):
        """Can we add a user?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/signup", data={"username": "testuser2",
                                            "email": "test2@test.com",
                                            "password": "testuser2",
                                            "image_url": None})

            self.assertEqual(resp.status_code, 302)


            user = User.query.filter_by(username="testuser2").first()

            self.assertEqual(user.username, "testuser2")

    def test_invalid_username_add_user(self):
        """Can we add a user?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/signup", data={"username": "",
                                            "email": "test2@test.com",
                                            "password": "testuser2",
                                            "image_url": None})

            self.assertEqual(resp.status_code, 200)


            user = User.query.filter_by(username="testuser2").first()

            self.assertFalse(user)
    
    def test_invalid_email_add_user(self):
        """Can we add a user?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/signup", data={"username": "jpri22",
                                            "email": "",
                                            "password": "testuser2",
                                            "image_url": None})

            self.assertEqual(resp.status_code, 200)


            user = User.query.filter_by(username="testuser2").first()

            self.assertFalse(user)
    
    def test_invalid_password_add_user(self):
        """Can we add a user without a password?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/signup", data={"username": "jpri22",
                                            "email": "justin10price@gmail.com",
                                            "password": "testuser2",
                                            "image_url": None})

            self.assertEqual(resp.status_code, 302)


            user = User.query.filter_by(username="testuser2").first()

            self.assertFalse(user)

    def test_delete_user(self):
        """Can we add a user?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            u = User(username="testuser2",
                 email="test@testmail.com",
                 password="testuser2",
                 image_url=None)

            db.session.add(u)
            db.session.commit()
            
            resp = c.post("/users/delete")
            
            self.assertEqual(resp.status_code, 302)


            user = User.query.filter_by(username="testuser2").first()

            self.assertEqual(user.username, "testuser2")


    def test_delete_user(self):
        """Can we add a user?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            u = User(username="testuser2",
                 email="test@testmail.com",
                 password="testuser2",
                 image_url=None)

            db.session.add(u)
            db.session.commit()
            
            resp = c.post("/users/delete")
            
            self.assertEqual(resp.status_code, 302)


            user = User.query.filter_by(username="testuser2").first()

            self.assertEqual(user.username, "testuser2")


