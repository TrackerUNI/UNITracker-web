from django.test import (
    TestCase,
    Client
)
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from  random import randint

from tracker.models import User, Position, Group


class TestUserPositionManagerView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_missed_user(self):
        data = {
            # missed user parameter
            'longitude': 30.2,
            'latitude': 1.23
        }


        r = self.client.post('/api/position/', data=data)
        #import pdb; pdb.set_trace()
        expected = {
                'user': ErrorDetail(string="This field is required",
                                    code='required')
            }

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data, expected)


    def test_bad_request(self):
        pk = '001'
        User.objects.create(user_id=pk, name='Luis')
        data = {
            'user': pk,
            'longtude': 30.2, # typo: longtude -> longitude
            'latitude': 1.23
        }

        r = self.client.post('/api/position/', data=data)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_not_exist(self):
        pk = '-1'
        data = {
            'user': pk, # invalid user id
            'longitude': 30.2,
            'latitude': 1.23
        }

        r = self.client.post('/api/position/', data=data)

        expected = {
            'user': ErrorDetail(string=f"Invalid pk '{pk}' - object does not exist",
                                code='does_not_exist')
        }

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.data, expected)


class TestUserPositionDetails(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_not_exist(self):
        pk = '-1'

        r = self.client.get(f"/api/position/{pk}/")

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_last_position(self):
        pk = '000001A'
        User.objects.create(user_id=pk, name='Alice')

        position_data = {
            'user': pk,
            'latitude': 20.3,
            'longitude': -10.5
        }

        # load las position of user 'Alice'
        self.client.post('/api/position/', data=position_data)

        r = self.client.get(f'/api/position/{pk}/')

        self.assertEqual(r.status_code, status.HTTP_200_OK)

        latitude = float(r.data['latitude'])
        longitude = float(r.data['longitude'])
        user = r.data['user']


        self.assertEqual(user, position_data['user'])
        self.assertAlmostEqual(latitude, position_data['latitude'])
        self.assertAlmostEqual(longitude, position_data['longitude'])
