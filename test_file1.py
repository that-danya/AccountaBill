from flask import Flask
from flask_testing import TestCase
import unittest
import server

class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app


class MyAppIntegrationTestCase(unittest.TestCase):
    """Testing Flask server."""

    def setUp(self):
        print "(setUp ran)"
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def tearDown(self):
        print "(tearDown ran)"

    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('<h1>AccountaBill</h1>', result.data)

    def test_register_button(self):
        client = server.app.test_client()
        result = client.get('/register', data={'session[user_id]': 1})
        self.assertIn('Please use no special characters!', result.data)

    def test_login(self):
        client = server.app.test_client()
        result = client.get('/login')
        self.assertIn('Login', result.data)

    def test_login_route(self):
        client = server.app.test_client()
        result = client.post('/login', data={'email':'a@a.com',
                                            'password': 'a'})
        self.assertIn('You have been logged in!', result.data)
 
if __name__ == "__main__":
    unittest.main()