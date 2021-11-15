from django.test import TestCase

from api.serializers import UserSerializer
from tracker.models import User, Position, Group

class TestSerialization(TestCase):

    def setUp(self):
        self.user_data = {'user_id': '1', 'name': 'Juan'}
        self.user = User.objects.create(**self.user_data)

    def test_serialization(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(self.user_data, serializer.data)
