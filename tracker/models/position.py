from django.db import models

from .user import User

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    latitude = models.DecimalField(max_digits=5, decimal_places=3)
    time = models.DateTimeField(auto_now=True)


    class Model:
        ordening = ['time']
