# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 00:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdbapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
                ('biography', models.TextField()),
                ('image', models.URLField()),
                ('birth_notes', models.TextField()),
                ('movie_list', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='search',
            options={'ordering': ['-id']},
        ),
    ]