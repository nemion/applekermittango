# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-09 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20170809_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='manual',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]