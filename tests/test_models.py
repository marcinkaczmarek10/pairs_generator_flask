import unittest
from website import create_app
from website.database.DB import SessionFactory, SessionContextManager
from website.database.models import User, RandomPerson, RandomPair, DrawCount
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
        self.first_person = RandomPerson(random_person_name='Janusz',
                                         random_person_email='janusz@testmail.com',
                                         user_id=1)
        self.second_person = RandomPerson(random_person_name='Mirek',
                                          random_person_email='mirek@testmail.com',
                                          user_id=1)
        with SessionContextManager() as session:
            session.add(self.first_person)
            session.add(self.second_person)

    @classmethod
    def setUpClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_exist_in_db(self):
        self.query_desc = SessionFactory.session.query(RandomPerson).order_by(RandomPerson.id.desc()).first()
        self.query_asc = SessionFactory.session.query(RandomPerson).order_by(RandomPerson.id.asc()).first()
        self.assertEqual(self.second_person.random_person_name, self.query_desc.random_person_name)
        self.assertEqual(self.first_person.random_person_name, self.query_asc.random_person_name)

    def test_delete_from_db(self):
        with SessionContextManager() as session:
            session.delete(self.first_person)
            session.delete(self.second_person)
        self.query = SessionFactory.session.query(RandomPerson).first()
        self.assertIsNone(self.query)

    def test_wrong_user_query(self):
        self.query = SessionFactory.session.query(RandomPerson).filter_by(user_id=2).first()
        self.assertIsNone(self.query)


class RandomPairTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.first_pair = RandomPair(first_person_name='Janusz',
                                     first_person_email='janusz@testmail.com',
                                     second_person_name='Mirek',
                                     second_person_email='mirek@testmail.com',
                                     draw_count=1)
        self.second_pair = RandomPair(first_person_name='Mirek',
                                      first_person_email='mirek@testmail.com',
                                      second_person_name='Janusz',
                                      second_person_email='janusz@testmail.com',
                                      draw_count=1)
        self.third_pair = RandomPair(first_person_name='Kornelia',
                                     first_person_email='kornelia@testmail.com',
                                     second_person_name='Gracja',
                                     second_person_email='gracja@testmail.com',
                                     draw_count=2)
        self.fourth_pair = RandomPair(first_person_name='Kornelia',
                                      first_person_email='kornelia@testmail.com',
                                      second_person_name='Gracja',
                                      second_person_email='gracja@testmail.com',
                                      draw_count=2)
        with SessionContextManager() as session:
            session.add(self.first_pair)
            session.add(self.second_pair)
            session.add(self.third_pair)
            session.add(self.fourth_pair)

    @classmethod
    def setUpClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_exist_in_db(self):
        self.query_first = SessionFactory.session.query(RandomPair).\
            filter_by(draw_count=1).order_by(RandomPair.id.desc()).first()
        self.query_second = SessionFactory.session.query(RandomPair).\
            filter_by(draw_count=2).order_by(RandomPair.id.desc()).first()
        self.assertEqual(self.second_pair.first_person_name, self.query_first.first_person_name)
        self.assertEqual(self.fourth_pair.first_person_name, self.query_second.first_person_name)

    def test_delete_from_db(self):
        with SessionContextManager() as session:
            session.delete(self.first_pair)
            session.delete(self.third_pair)
            session.delete(self.second_pair)
            session.delete(self.fourth_pair)
        self.query = SessionFactory.session.query(RandomPair).filter_by(draw_count=1).first()
        self.assertIsNone(self.query)
        self.query_second = SessionFactory.session.query(RandomPair).filter_by(draw_count=2).first()
        self.assertIsNone(self.query_second)


class DrawCountTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.first_count = DrawCount(user_id=1)
        self.second_count = DrawCount(user_id=1)
        with SessionContextManager() as session:
            session.add(self.first_count)
            session.add(self.second_count)

    @classmethod
    def setUpClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_exist_in_db(self):
        self.query_desc = SessionFactory.session.query(DrawCount).order_by(DrawCount.id.desc()).first()
        self.query_asc = SessionFactory.session.query(DrawCount).order_by(DrawCount.id.asc()).first()
        self.assertEqual(self.second_count.id, self.query_desc.id)
        self.assertEqual(self.first_count.id, self.query_asc.id)

    def test_delete_from_db(self):
        with SessionContextManager() as session:
            session.delete(self.first_count)
            session.delete(self.second_count)
        self.query = SessionFactory.session.query(DrawCount).first()
        self.assertIsNone(self.query)

    def test_wrong_user_query(self):
        self.query = SessionFactory.session.query(DrawCount).filter_by(user_id=2).first()
        self.assertIsNone(self.query)


class DrawPairRelationshipTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.first_count = DrawCount(user_id=1)
        self.second_count = DrawCount(user_id=2)
        self.first_pair = RandomPair(first_person_name='Janusz',
                                     first_person_email='janusz@testmail.com',
                                     second_person_name='Mirek',
                                     second_person_email='mirek@testmail.com',
                                     draw_count=1)
        self.second_pair = RandomPair(first_person_name='Mirek',
                                      first_person_email='mirek@testmail.com',
                                      second_person_name='Janusz',
                                      second_person_email='janusz@testmail.com',
                                      draw_count=1)
        self.third_pair = RandomPair(first_person_name='Kornelia',
                                     first_person_email='kornelia@testmail.com',
                                     second_person_name='Gracja',
                                     second_person_email='gracja@testmail.com',
                                     draw_count=2)
        self.fourth_pair = RandomPair(first_person_name='Kornelia',
                                      first_person_email='kornelia@testmail.com',
                                      second_person_name='Gracja',
                                      second_person_email='gracja@testmail.com',
                                      draw_count=2)
        with SessionContextManager() as session:
            session.add(self.first_count)
            session.add(self.second_count)
            session.add(self.first_pair)
            session.add(self.second_pair)
            session.add(self.third_pair)
            session.add(self.fourth_pair)

    @classmethod
    def setUpClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_exist_in_db(self):
        self.first_query = SessionFactory.session.query(RandomPair).\
            outerjoin(DrawCount, RandomPair.draw_count == DrawCount.id).\
            filter(DrawCount.user_id == 1).order_by(RandomPair.id.desc()).first()

        self.second_query = SessionFactory.session.query(RandomPair).\
            outerjoin(DrawCount, RandomPair.draw_count == DrawCount.id).\
            filter(DrawCount.user_id == 2).order_by(RandomPair.id.desc()).first()

        self.assertEqual(self.second_pair.id, self.first_query.id)
        self.assertEqual(self.fourth_pair.id, self.second_query.id)

    def test_nonexisting_user_query(self):
        self.query = SessionFactory.session.query(RandomPair).\
            outerjoin(DrawCount, RandomPair.draw_count == DrawCount.id).\
            filter(DrawCount.user_id == 3).first()

        self.assertIsNone(self.query)

    def test_wrong_user(self):
        self.query = SessionFactory.session.query(RandomPair).\
            outerjoin(DrawCount, RandomPair.draw_count == DrawCount.id).\
            filter(DrawCount.user_id == 2).first()

        self.assertNotEqual(self.first_pair.id, self.query.id)
