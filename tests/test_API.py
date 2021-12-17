import json
import unittest
from website import create_app
from website.database.DB import SessionFactory, SessionContextManager
from website.config import TestingConfig
from website.database.models import User, RandomPerson
import base64


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.user = SessionFactory.session.query(User).filter_by(email='user@testmail.com').first()
        self.token = self.user.get_token()
        self.pair = SessionFactory.session.query(RandomPerson).filter_by(random_person_name='Janusz').first()

    @classmethod
    def setUpClass(cls) -> None:
        SessionFactory.Base.metadata.create_all(SessionFactory.engine)
        user = User(username='user',
                    email='user@testmail.com',
                    password='test')
        pair = RandomPerson(random_person_name='Janusz',
                            random_person_email='janusz@testmail.com')
        with SessionContextManager() as session:
            session.add(user)
            session.add(pair)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls) -> None:
        SessionFactory.Base.metadata.drop_all(SessionFactory.engine)

    def test_api_auth(self):
        credentials = base64.b64encode(b"user:test").decode('utf-8')
        res = self.client.get('/api/login', headers={'Authorization': 'Basic Og' + credentials})
        self.assertEqual(res.status_code, 200)

    def test_no_auth(self):
        res = self.client.get('api/login')
        self.assertEqual(res.status_code, 401)

    def test_get_results(self):
        res = self.client.get('api/results', headers={'api_key': self.token})
        self.assertEqual(res.status_code, 200)

    def test_get_pairs(self):
        res = self.client.get('api/pairs', headers={'api_key': self.token})
        self.assertEqual(res.status_code, 200)

    def test_post_generate_pairs(self):
        data = json.dumps([{'random_person_name': 'Janusz',
                            'random_person_email': 'janusz@testmail.com'},
                           {'random_person_name': 'Mirek',
                            'random_person_email': 'mirek@testmail.com'}])
        res = self.client.post('api/generate-pairs',
                               headers={'api_key': self.token, 'Content-Type': 'application/json'},
                               data=data)
        self.assertEqual(res.status_code, 200)

    def test_generate_pairs_fail(self):
        data = json.dumps([{'random_person_name': 'Janusz',
                            'random_person_email': 'janusz@testmail.com'}])
        res = self.client.post('api/generate-pairs',
                               headers={'api_key': self.token, 'Content-Type': 'application/json'},
                               data=data)
        self.assertEqual(res.status_code, 403)

    def test_delete_pair(self):
        data = json.dumps({'pair': self.pair.id})
        res = self.client.delete('api/delete-pair',
                                 headers={'api_key': self.token, 'Content-Type': 'application/json'},
                                 data=data)
        self.assertEqual(res.status_code, 200)

    def test_no_pair(self):
        data = json.dumps({'pair': '3'})
        res = self.client.delete('api/delete-pair',
                                 headers={'api_key': self.token, 'Content-Type': 'application/json'},
                                 data=data)
        self.assertEqual(res.status_code, 404)

    def test_send_email(self):
        pass

    def test_send_mail_fail(self):
        data = json.dumps({'draw_count': '',
                           'title': '',
                           'body': ''})
        res = self.client.post('/api/send-email',
                               headers={'api_key': self.token, 'Content-Type': 'application/json'},
                               data=data)
        self.assertEqual(res.status_code, 404)

    def test_no_token_get_result(self):
        res = self.client.get('api/results')
        self.assertEqual(res.status_code, 401)

    def test_no_token_get_pairs(self):
        res = self.client.get('api/pairs')
        self.assertEqual(res.status_code, 401)

    def test_no_token_post_generate_pairs(self):
        res = self.client.post('api/generate-pairs')
        self.assertEqual(res.status_code, 401)

    def test_no_token_delete_pairs(self):
        res = self.client.delete('api/delete-pair')
        self.assertEqual(res.status_code, 401)

    def test_no_token_delete_results(self):
        res = self.client.delete('api/delete-results')
        self.assertEqual(res.status_code, 401)

    def test_no_token_send_mails(self):
        res = self.client.post('api/send-email')
        self.assertEqual(res.status_code, 401)
