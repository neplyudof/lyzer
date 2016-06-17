# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memsis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dumpinfo',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='dumpinfo',
            name='file_path',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='dumpinfo',
            name='profile',
            field=models.CharField(default='', max_length=50),
        ),
    ]
