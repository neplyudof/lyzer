# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class DumpInfo(models.Model):
    file_name = models.CharField(max_length=50, default='')
    file_path = models.CharField(max_length=50, default='')
    profile = models.CharField(max_length=50, default='')
    description = models.TextField(default='')

    def __unicode__(self):
        return self.file_name


class ImageInfo(models.Model):
    # [[columns]]
    # suggested_profile - 문자열 100
    # as_layer1 - 문자열 100
    # as_layer2 - 문자열 100
    # pae_type - 문자열 10
    # dtb - 정수
    # kdbg - 정수
    # number_of_processors - 정수
    # image_type_ - 정수
    # kpcr_for_cpu_0 - 정수
    # kuser_shared_data - 정수
    # image_date_and_time - date
    # image_local_date_and_time - date
    dump_info = models.ForeignKey(DumpInfo, on_delete=models.CASCADE)
    suggested_profile = models.CharField(max_length=100, default='')
    as_layer1 = models.CharField(max_length=100, default='')
    as_layer2 = models.CharField(max_length=100, default='')
    pae_type = models.CharField(max_length=10, default='')
    dtb = models.BigIntegerField(default=0)
    kdbg = models.BigIntegerField(default=0)
    number_of_processors = models.PositiveSmallIntegerField(default=0)
    image_type = models.PositiveSmallIntegerField(default=0)
    kpcr_for_cpu_0 = models.BigIntegerField(default=0)
    kuser_shared_data = models.BigIntegerField(default=0)
    image_date_and_time = models.CharField(max_length=100, default='')
    image_local_data_and_time = models.CharField(max_length=100, default='')

    def update_key(self, key, value):
        self.__setattr__(key, value)

    def __setattr__(self, key, value):
        super(ImageInfo, self).__setattr__(key, value)