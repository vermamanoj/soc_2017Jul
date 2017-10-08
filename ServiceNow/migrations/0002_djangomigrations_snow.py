# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServiceNow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Snow',
            fields=[
                ('uid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('snow_url', models.TextField()),
                ('user', models.TextField()),
                ('pwd', models.TextField()),
                ('table', models.TextField()),
                ('category', models.TextField()),
                ('sub_category', models.TextField()),
            ],
            options={
                'db_table': 'snow',
                'managed': False,
            },
        ),
    ]