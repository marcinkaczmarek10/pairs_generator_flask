import unittest
from website import create_app
from website.database.DB import SessionFactory
from website.database.models import User, RandomPerson, RandomPair, DrawCount, WhichCount
from website.config import TestingConfig


class UserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)
        self.user = User(username='user',
                         email='user@testmail.com',
                         password='test')

    def tearDown(self):
        self.app_context.pop()
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_create_user(self):
        self.assertFalse(self.user.password is None)
        self.assertFalse(self.user.username is None)
        self.assertFalse(self.user.email is None)

    def test_user_verification(self):
        self.assertTrue(self.user.password == 'test')
        self.assertTrue(self.user.username == 'user')
        self.assertTrue(self.user.email == 'user@testmail.com')
        self.assertFalse(self.user.password == 'dog')
        self.assertFalse(self.user.username == 'dog')
        self.assertFalse(self.user.email == 'dog')

    def test_generate_token(self):
        token = self.user.get_token()
        self.assertTrue(token is not None)

    def test_load_user_from_token(self):
        token = self.user.get_token()
        user_id = self.user.verify_token(token)
        self.assertEqual(self.user.id, user_id)


class RandomPersonTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)


class RandomPairTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)


class DrawCountTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)
