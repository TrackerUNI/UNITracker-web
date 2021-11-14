from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True) # remove null values (ONLY FOR TEST)

    @staticmethod
    def exists(user_id):
        try:
            User.objects.get(pk = user_id)
            return True

        except User.DoesNotExist:
            return False
