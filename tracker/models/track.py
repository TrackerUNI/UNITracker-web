from django.db import models

from .user import User
from .group import Group

class Track(models.Model):
    # a user can track many groups
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
