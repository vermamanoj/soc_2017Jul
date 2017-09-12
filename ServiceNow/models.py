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






