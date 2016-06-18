# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memsis', '0002_auto_20160617_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='dumpinfo',
            name='file_name',
            field=models.TextField(default=''),
        ),
    ]
