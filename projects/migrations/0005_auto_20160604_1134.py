# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-04 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_activity_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
