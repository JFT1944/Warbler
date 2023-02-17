
import os
from unittest import TestCase

from models import db, User, Message, Follows


os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app


db.create_all()


class messageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u= User(
            email="test@testmail.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()


    def test_message_model(self):
        """Does message model work?"""
        u = User.query.getALL()
        m = Message(
            text="test message",
            user_id=u[0].id      
             )

        db.session.add(m)
        db.session.commit()

        new_m = Message.query.get(39)

        # User should have no messages & no followers
        self.assertEqual(new_m.text, 'test message')
        self.assertEqual(new_m.user_id, u,id)

        
    def test_invalid_message_text_model(self):
        """Does message model work?"""
        
       

        m = Message(
            text="",
            user_id=208
        )

        db.session.add(m)
        db.session.commit()

        new_m = Message.query.get(39)

        # User should have no messages & no followers
        self.assertFalse(new_m)

        
    def test_invalid_message_userid_model(self):
        """Does message model work?"""
        
        m = Message(
            text="hola",
            user_id="208"
        )

        db.session.add(m)
        db.session.commit()

        new_m = Message.query.get(39)

        # User should have no messages & no followers
        self.assertFalse(new_m)

        

        
    def tearDown(self):
        db.session.rollback()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.commit()