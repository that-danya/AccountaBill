import server
import unittest


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

    

if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()
