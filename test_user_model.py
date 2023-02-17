"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

# Does User.create successfully create a new user given valid credentials?
# Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?

    def test_repr(self):
        """Does the repr method work as expected?"""

        u = User(
            email="jp@gmail.com",
            username="jp",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(repr(u), f"<User #{u.id}: {u.username}, {u.email}>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""

        u1 = User(
            email="jp@gmail.com",
            username="jp",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="mr@gmail.com",
            username="mr",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        u1.following.append(u2)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), True)
        
    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""

        u1 = User(
            email="jprice@gmail.com",
            username="jprice",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="mr@gmail.com",
            username="mr",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.assertEqual(u1.is_following(u2), False)


    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        u1 = User(
            email="jprice@gmail.com",
            username="jprice",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="mr@gmail.com",
            username="mr",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        u2.following.append(u1)
        db.session.commit()

        self.assertEqual(u1.is_followed_by(u2), True)


    def test_user_create(self):
        """Does User.create successfully create a new user given valid credentials?"""

        u = User(
            email="jprice@gmail.com",
            username="jprice",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.email, "jprice@gmail.com")

    def test_user_create_fail(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        u = User(
            email="",
            username="jprice",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.add(u)
        db.session.commit()

        self.assertFalse(u.email)

    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        u = User.signup(
            email="jprice@gmail.com",
            username="jprice",
            password="HASHED_PASSWORD",
            image_url=None
        )
        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.authenticate("jprice", "HASHED_PASSWORD"), u)

