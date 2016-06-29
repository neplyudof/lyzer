# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memsis', '0004_auto_20160628_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suggested_profile', models.CharField(default='', max_length=100)),
                ('as_layer1', models.CharField(default='', max_length=100)),
                ('as_layer2', models.CharField(default='', max_length=100)),
                ('pae_type', models.CharField(default='', max_length=100)),
                ('dtb', models.BigIntegerField()),
                ('kdbg', models.BigIntegerField()),
                ('number_of_processors', models.PositiveSmallIntegerField()),
                ('service_pack', models.PositiveSmallIntegerField()),
                ('dump_info', models.ForeignKey(to='memsis.DumpInfo')),
            ],
        ),
    ]
