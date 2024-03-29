# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 07:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_personnel_level'),
        ('projects', '0006_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Personnel')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_description', models.CharField(max_length=100)),
                ('due_date', models.DateField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to='Users.Personnel')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to='Users.Personnel')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Tasks'),
        ),
    ]
