from django.test import TestCase
from django.db.models import Q

from tracker.models import User, Position

class TestUserModel(TestCase):

    def test_persistence(self):
        user = User.objects.create(user_id='1000')
        position_data = {
            'user': user,
            'latitude': -32.02,
            'longitude': 20.89
        }

        position = Position.objects.create(**position_data)

        query_position = Position.objects.get(
            user_id = position_data['user'],
            latitude = position_data['latitude'],
            longitude = position_data['longitude'],
        )

        self.assertEqual(position, query_position)
