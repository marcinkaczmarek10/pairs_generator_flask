import unittest
from flask import current_app
from website import create_app
from website.database.DB import SessionFactory, SessionContextManager
from website.config import TestingConfig
from website.database.models import User


class ClientAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        self.user = SessionFactory.session.query(User).filter_by(email='user@testmail.com').first()

    @classmethod
    def setUpClass(cls) -> None:
        SessionFactory.Base.metadata.create_all(SessionFactory.engine)
        user = User(username='user',
                    email='user@testmail.com',
                    password='test')
        with SessionContextManager() as session:
            session.add(user)

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls) -> None:
        SessionFactory.Base.metadata.drop_all(SessionFactory.engine)

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_app_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_register(self):
        res = self.client.post('/register', data={
            'username': 'user',
            'email': 'user@testmail.com',
            'password': 'test',
            'confirm_password': 'test'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_register_authenticated(self):
        pass

    def test_login(self):
        res = self.client.post('/login', data={
            'email': 'user@testmail.com',
            'password': 'test'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_reset_password(self):
        res_get = self.client.get('/reset-password', follow_redirects=True)
        res_post = self.client.post('/reset-password',
                                    data={'email': 'user@testmail.com'},
                                    follow_redirects=True)
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_post.status_code, 200)

    def test_reset_password_token(self):
        token = self.user.get_token()
        res_get = self.client.get(f'/reset-password/{token}', follow_redirects=True)
        res_post = self.client.post(f'/reset-password/{token}',
                                    data={'password': 'test', 'confirm_password': 'test'},
                                    follow_redirects=True
                                    )
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_post.status_code, 200)

    def test_confirm_mail(self):
        token = self.user.get_token()
        res_get = self.client.get(f'/confirm-email/{token}', follow_redirects=True)
        self.assertEqual(res_get.status_code, 200)

    def test_account(self):
        res_get = self.client.get('/account')
        res_post = self.client.post('/account', data={'password': 'test', 'confirm_password': 'test'})
        self.assertEqual(res_get.status_code, 302)
        self.assertEqual(res_post.status_code, 302)


class ClientAuthenticatedTestCase(unittest.TestCase):
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
        with SessionContextManager() as session:
            session.add(user)

    @classmethod
    def tearDownClass(cls) -> None:
        session = SessionFactory()
        SessionFactory.Base.metadata.drop_all(session.engine)

    def test_login(self):
        with self.client:
            res = self.client.get('/auto-login')
            self.assertEqual(res.status_code, 200)
            res_login = self.client.get('/login')
            self.assertEqual(res_login.status_code, 302)


    def test_register(self):
        with self.client:
            res = self.client.get('/auto-login')
            self.assertEqual(res.status_code, 200)
            res_login = self.client.get('/register')
            self.assertEqual(res_login.status_code, 302)

    def test_restet_passwrod(self):
        with self.client:
            res = self.client.get('/auto-login')
            self.assertEqual(res.status_code, 200)
            res_login = self.client.get('/reset-password')
            self.assertEqual(res_login.status_code, 302)

    def test_account(self):
        with self.client:
            res = self.client.get('/auto-login')
            self.assertEqual(res.status_code, 200)
            res_get = self.client.get('/account')
            res_post = self.client.post('/account', data={'password': 'test', 'confirm_password': 'test'})
            self.assertEqual(res_get.status_code, 200)
            self.assertEqual(res_post.status_code, 200)
