from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models

class customer1_incidents(models.Model):
    snow_id = models.CharField(max_length=20)
    number = models.CharField(max_length=10)
    state = models.IntegerField()
    category = models.CharField(max_length=20)
    priority = models.IntegerField()
    date_created = models.DateTimeField()
    opened_by = models.CharField(max_length=20)
    assigned_to = models.CharField(max_length=20)
    short_desc = models.CharField(max_length=30)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Snow(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    base_url = models.TextField()
    user = models.TextField()
    pwd = models.TextField()
    table = models.TextField()
    category = JSONField()  # This field type is a guess.
    sub_category = JSONField()  # This field type is a guess.
    assignment_group = JSONField()
    fields = models.TextField()

    class Meta:
        managed = False
        db_table = 'snow'




