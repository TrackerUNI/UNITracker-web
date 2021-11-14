from django.db import models

from .user import User

class Group(models.Model):
    group_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    users = models.ManyToManyField(User, blank=True)
