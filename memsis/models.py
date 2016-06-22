from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models


class DumpInfo(models.Model):
    file_name = models.CharField(max_length=50, default='')
    file_path = models.CharField(max_length=50, default='')
    profile = models.CharField(max_length=50, default='')
    description = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('memsis:home')

    def __unicode__(self):
        return self.file_name
