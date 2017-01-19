# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_personnel_level'),
        ('projects', '0009_tasks_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentVerbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verb', models.CharField(max_length=100)),
                ('classification', models.CharField(choices=[('Projects Department', 'Projects Department'), ('Marketing', 'Marketing'), ('Engineering', 'Engineering'), ('Fabrication', 'Fabrication'), ('Client', 'Client')], default='Projects Department', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalVerbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verb', models.CharField(max_length=100)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Personnel')),
            ],
        ),
    ]
