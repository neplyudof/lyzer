# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memsis', '0003_dumpinfo_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dumpinfo',
            name='file_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='dumpinfo',
            name='file_path',
            field=models.CharField(default='', max_length=50),
        ),
    ]
