# coding=utf-8

from django.test import TestCase

from memsis.models import DumpInfo


class DumpInfoModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_model = DumpInfo()
        first_model.file_path = '/Users/J/Documents/ExampleImage/1.vmem'
        first_model.profile = 'WinXPSP2x86'
        first_model.description = '첫 번째 덤프파일'
        first_model.save()

        second_model = DumpInfo()
        second_model.file_path = '/Users/J/Documents/ExampleImage/2.vmem'
        second_model.profile = 'Win7SP1x86'
        second_model.description = '두 번째 덤프파일'
        second_model.save()

        saved_model = DumpInfo.objects.all()
        self.assertEqual(saved_model.count(), 2)

        first_saved_model = saved_model[0]
        second_saved_model = saved_model[1]

        self.assertEqual(first_saved_model.file_path, u'/Users/J/Documents/ExampleImage/1.vmem')
        self.assertEqual(first_saved_model.profile, 'WinXPSP2x86')
        self.assertEqual(first_saved_model.description, u'첫 번째 덤프파일')

        self.assertEqual(second_saved_model.file_path, u'/Users/J/Documents/ExampleImage/2.vmem')
        self.assertEqual(second_saved_model.profile, u'Win7SP1x86')
        self.assertEqual(second_saved_model.description, u'두 번째 덤프파일')
