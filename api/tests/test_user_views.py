from django.test import (
    TestCase,
    Client
)
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from  random import randint

from tracker.models import User, Position, Group

class TestUserManager(TestCase):
    def setUp(self):
        self.client = Client()

    def test_missed_user_id(self):
        data = {
            # missed user_id parameter
            'name': 'Luisa'
        }


        r = self.client.post('/api/user/', data=data)
        #import pdb; pdb.set_trace()
        expected = {
                'user_id': ErrorDetail(string="This field is required",
                                       code='required')
            }

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data, expected)

    def test_new_user(self):
        pk = '000001B'
        data = {
            'user_id': pk, # user does not exist
            'name': 'Pepe',
        }

        r = self.client.post('/api/user/', data=data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        user = self.client.get(f"/api/user/{pk}/")
        self.assertEqual(user.status_code, status.HTTP_200_OK)

        self.assertEqual(r.data, user.data)

    def test_bad_request(self):

        pk = '00000C'
        data = {
            'usr_id': pk, # typo: usr_id -> user_id
            'name': f'user-{pk}'
        }

        r = self.client.post('/api/user/', data=data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
