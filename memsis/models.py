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
    dump_info = models.ForeignKey(DumpInfo)
    suggested_profile = models.CharField(max_length=100, default='')
    as_layer1 = models.CharField(max_length=100, default='')
    as_layer2 = models.CharField(max_length=100, default='')
    pae_type = models.CharField(max_length=10, default='')
    dtb = models.BigIntegerField()
    kdbg = models.BigIntegerField()
    number_of_processors = models.PositiveSmallIntegerField()
    image_type = models.PositiveSmallIntegerField()
    kpcr_for_cpu_0 = models.BigIntegerField()
    kuser_shared_data = models.BigIntegerField()
    image_date_and_time = models.DateTimeField()
    image_local_data_and_time = models.DateTimeField()

    def update_key(self, key, value):
        self.__setattr__(key, value)

    def __setattr__(self, key, value):
        super(ImageInfo, self).__setattr__(key, value)