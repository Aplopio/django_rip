"""
Models to run integration tests
"""
from django.db import models


class TestPersonModel(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

    class Meta:
        app_label = 'tests'
