import unittest
from flask import current_app
from website import create_app
from website.database.DB import SessionFactory
from website.config import TestingConfig
from website.database.models import User


class ClientAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        SessionFactory.Base.metadata.create_all(SessionFactory.engine)
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

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
        })
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
        res_post = self.client.post('/reset-password', data={'email': 'user@testmail.com'})
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_post.status_code, 302)

    def test_reset_password_token(self):
        user = SessionFactory.session.query(User).filter_by(email='user@testmail.com').first()
        token = user.get_token()
        res_get = self.client.get(f'/reset-password/{token}', follow_redirects=True)
        res_post = self.client.post(f'/reset-password/{token}',
                                    data={'password': 'test', 'confirm_password': 'test'},
                                    follow_redirects=True
                                    )
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_post.status_code, 200)

    def test_confirm_mail(self):
        user = SessionFactory.session.query(User).filter_by(email='user@testmail.com').first()
        token = user.get_token()
        res_get = self.client.get(f'/confirm-email/{token}', follow_redirects=True)
        self.assertEqual(res_get.status_code, 200)

    def test_account(self):
        res_get = self.client.get('/account')
        res_post = self.client.post('/account', data={'password': 'test', 'confirm_password': 'test'})
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_post.status_code, 200)
