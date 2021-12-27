import unittest
import json
from website import create_app
from website.database.DB import SessionFactory, SessionContextManager
from website.config import TestingConfig
from website.database.models import User, UsersPerson, RandomPair
from website.utils.data_serializers import ResultSchema


class ClientGeneratePairsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def setUpClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.create_all(session.engine)
        user = User(username='user',
                    email='user@testmail.com',
                    password='test')
        person = UsersPerson(person_name='Mirek',
                             person_email='mirek@testmail.com')
        random_pairs = RandomPair(
            first_person_name='janusz',
            first_person_email='janusz@tetmail.com',
            second_person_name='mirek',
            second_person_email='mirek@testmail.com',
            draw_count='2'
        )
        with SessionContextManager() as session:
            session.add(user)
            session.add(person)
            session.add(random_pairs)

    @classmethod
    def tearDownClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_generate_pairs(self):
        with self.client:
            self.client.get('/auto-login')
            res_get = self.client.get('/generate-pairs')
            self.assertEqual(res_get.status_code, 200)
            res_post = self.client.post('/generate-pairs', data={
                'person_name': 'Janusz',
                'person_email': 'janusz@testmail.com'},
                             follow_redirects=True)
            self.assertEqual(res_post.status_code, 200)

    def test_results(self):
        with self.client:
            self.client.get('/auto-login')
            res = self.client.post('/results', follow_redirects=True)
            self.assertEqual(res.status_code, 200)

    def test_show_results(self):
        with self.client:
            self.client.get('/auto-login')
            res = self.client.get('/show-results')
            self.assertEqual(res.status_code, 200)

    def test_submit_result(self):
        data = json.dumps([{'draw_count': 2}, {'draw_count': 2}])
        with self.client:
            self.client.get('/auto-login')
            res = self.client.post('/submit-result',
                                   data=data)
            self.assertEqual(res.status_code, 200)

    def test_delete_result(self):
        data_query = SessionFactory.session.query(RandomPair).filter_by(draw_count='2').all()
        schema = ResultSchema()
        data = json.dumps(schema.dump(data_query))
        with self.client:
            self.client.get('/auto-login')
            res = self.client.post('/delete-result',
                                   data=data)
            self.assertEqual(res.status_code, 200)

    def test_send_mail_get_fail(self):
        with self.client:
            self.client.get('/auto-login')
            res = self.client.get('/submit-sending-email')
            self.assertEqual(res.status_code, 302)

    def test_delete_person(self):
        with self.client:
            self.client.get('/auto-login')
            res = self.client.post('/delete-person', follow_redirects=True)
            self.assertEqual(res.status_code, 200)

    def test_send_mail(self):
        data = {'email_title': 'ttile', 'email_body': 'body'}
        with self.client:
            self.client.get('/auto-login')
            res = self.client.post('/submit-sending-email',
                                   follow_redirects=True,
                                   data=data)
            self.assertEqual(res.status_code, 200)
