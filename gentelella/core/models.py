# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals
from django.db import models

class Pessoa(models.Model):
    pass

class CustomerInfo(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    customer_name = models.TextField()  # This field type is a guess.
    customer_location = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'customer_info'