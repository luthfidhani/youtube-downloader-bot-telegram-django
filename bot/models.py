from django.db import models

class Users(models.Model):
    id = models.BigIntegerField(primary_key=True)
    url = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
