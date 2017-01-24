# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_term', models.CharField(max_length=100)),
                ('attribute', models.CharField(choices=[('movie', 'movie'), ('actor', 'actor')], default='movie', max_length=30)),
            ],
        ),
    ]