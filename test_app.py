import unittest
import sqlite3
import os
from app import app, init_db

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Setup test client and test database
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        # Re-initialize DB before each test
        if os.path.exists("database.db"):
            os.remove("database.db")
        init_db()

    def register_user(self, username, password):
        return self.client.post('/register', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def login_user(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_register(self):
        response = self.register_user("testuser", "password123")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_duplicate_register(self):
        self.register_user("testuser", "password123")
        response = self.register_user("testuser", "password123")
        self.assertIn(b'Username already exists!', response.data)

    def test_login_success(self):
        self.register_user("testuser", "password123")
        response = self.login_user("testuser", "password123")
        self.assertIn(b'Dashboard', response.data)

    def test_login_failure(self):
        response = self.login_user("fakeuser", "wrongpass")
        self.assertIn(b'Invalid credentials', response.data)

    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect to /login

if __name__ == '__main__':
    unittest.main()
