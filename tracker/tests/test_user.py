from django.test import TestCase

from tracker.models import User

class TestUserModel(TestCase):

    def test_user_exists(self):
        user_data = {
            'user_id': '1000',
            'name': 'Carlos'
        }

        User.objects.create(**user_data)

        self.assertTrue(User.exists(user_data['user_id']))
