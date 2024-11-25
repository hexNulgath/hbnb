import unittest
import json
from app import create_app, db

class TestHBnBAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config.TestingConfig')  # Use a testing configuration
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()  # Create the database tables

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()  # Drop the database tables
        cls.app_context.pop()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_create_place(self):
        # First, create a user and log in to get a JWT token
        self.test_create_user()
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        token = login_response.get_json()['access_token']

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "1"
        }, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 201)

    def test_get_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_create_review(self):
        # Create a place first
        self.test_create_place()
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        token = login_response.get_json()['access_token']

        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": "1",
            "place_id": "1"
        }, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 201)

    def test_get_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        response = self.client.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()