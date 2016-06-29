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


class ImageInfo(models.Model):
    dump_info = models.ForeignKey(DumpInfo)
    suggested_profile = models.CharField(max_length=100, default='')
    as_layer1 = models.CharField(max_length=100, default='')
    as_layer2 = models.CharField(max_length=100, default='')
    pae_type = models.CharField(max_length=100, default='')
    dtb = models.BigIntegerField()
    kdbg = models.BigIntegerField()
    number_of_processors = models.PositiveSmallIntegerField()
    service_pack = models.PositiveSmallIntegerField()
