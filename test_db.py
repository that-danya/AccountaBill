from flask_testing import TestCase
import unittest
from server import app, db

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "postgresql://tests"
    TESTING = True

    def create_app(self):

        def test_index(self):
            client = server.app.test_client()
            result = client.get('/')
            self.assertIn('<h1>AccountaBill</h1>', result.data)

        def test_register_button(self):
            client = server.app.test_client()
            result = client.get('/register', data={'session[user_id]': 1})
            self.assertIn('Please use no special characters!', result.data)

        return create_app(self)

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
    

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()