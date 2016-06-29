# coding=utf-8
from crispy_forms.helper import FormHelper
from django import forms

from memsis.models import DumpInfo
from memsis.volinterface import profile_list

EMPTY_FILE_PATH_ERROR = u'유효한 파일 경로를 입력해주세요'
FILE_PATH_PLACEHOLDER = u'메모리 덤프파일 절대 경로 입력'


class DumpInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DumpInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = u'col-xs-2 col-lg-2 col-md-2'
        self.helper.field_class = u'col-xs-10 col-lg-10 col-md-10'

    # Todo: 폼 검증 루틴 추가하기
    class Meta:
        model = DumpInfo
        fields = ('file_path', 'profile', 'description',)
        widgets = {
            'file_path': forms.TextInput(attrs={'placeholder': FILE_PATH_PLACEHOLDER}),
            'profile': forms.Select(attrs={u'class': u'select'},
                                    choices=[(prof, prof) for prof in profile_list()]),
        }
        error_messages = {
            'file_path': {'required': EMPTY_FILE_PATH_ERROR}
        }
