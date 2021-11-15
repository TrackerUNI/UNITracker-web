from django.test import (
    TestCase,
    Client
)
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from  random import randint

from tracker.models import User, Position, Group

class TestUserManager(TestCase):
    pass
