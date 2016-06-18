from __future__ import unicode_literals

from django.db import models


class DumpInfo(models.Model):
    file_name = models.TextField(default='')
    file_path = models.TextField(default='')
    profile = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
