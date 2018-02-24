from django.db import models

# Create your models here.


class update(models.Model):
    version = models.CharField(max_length=20)
    time = models.TimeField()
