# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-20 13:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20160420_1626'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=100)),
                ('classification', models.CharField(choices=[('Projects Department', 'Projects Department'), ('Marketing', 'Marketing'), ('Engineering', 'Engineering'), ('Fabrication', 'Fabrication'), ('Client', 'Client')], default='Projects Department', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('proj_rev', models.CharField(max_length=1)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Activity')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Personnel')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
