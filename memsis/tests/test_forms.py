# coding=utf-8
from django.test import TestCase

from memsis.forms import DumpInfoForm


class DumpInfoFormTest(TestCase):
    def test_form_validation_for_blank_file_path(self):
        form = DumpInfoForm(data={'file_path': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['file_path'],
            [u'유효한 파일 경로를 입력해주세요']
        )
