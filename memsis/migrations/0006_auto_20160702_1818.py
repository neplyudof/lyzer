# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memsis', '0005_imageinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageinfo',
            name='service_pack',
        ),
        migrations.AddField(
            model_name='imageinfo',
            name='image_date_and_time',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='imageinfo',
            name='image_local_data_and_time',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='imageinfo',
            name='image_type',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imageinfo',
            name='kpcr_for_cpu_0',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='imageinfo',
            name='kuser_shared_data',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='imageinfo',
            name='dtb',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='imageinfo',
            name='kdbg',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='imageinfo',
            name='number_of_processors',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='imageinfo',
            name='pae_type',
            field=models.CharField(default='', max_length=10),
        ),
    ]
