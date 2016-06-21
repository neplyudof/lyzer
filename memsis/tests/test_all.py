# coding=utf-8
from unittest import skip
from urlparse import urlparse

from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from memsis import views
from memsis.models import DumpInfo
from memsis.views import index_page


@skip
class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)


class MainPageTest(TestCase):
    def test_root_url_resolve(self):
        root_url = resolve('/')

        self.assertEqual(root_url.func, views.index_page)

    def test_returns_correct_main_page(self):
        request = HttpRequest()
        response = views.index_page(request)
        expected_html = render_to_string('index.html')

        self.assertEqual(expected_html, response.content.decode('utf-8'))

    def test_index_page_can_save_POST_request(self):
        file_path = '/Users/J/Documents/ExampleImage/1.vmem'
        file_name = '1.vmem'
        profile = 'AutoDetect'
        description = 'test'

        self.client.post(
            reverse('memsis:home'),
            data={
                'file_path': file_path,
                'profile': profile,
                'description': description
            }
        )

        self.assertEqual(DumpInfo.objects.count(), 1)
        saved_model = DumpInfo.objects.first()
        self.assertEqual(saved_model.file_name, file_name)
        self.assertEqual(saved_model.file_path, file_path)
        self.assertEqual(saved_model.profile, profile)
        self.assertEqual(saved_model.description, description)

    def test_index_page_redirects_after_POST(self):
        file_path = '/Users/J/Documents/ExampleImage/1.vmem'
        profile = 'AutoDetect'
        description = 'test'

        response = self.client.post(
            reverse('memsis:home'),
            data={
                'file_path': file_path,
                'profile': profile,
                'description': description
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response['location']).path, reverse('memsis:home'))

    def test_index_page_displays_all_list_items(self):
        DumpInfo.objects.create(
            file_path='path1',
            profile='profile1',
            description='test1'
        )
        DumpInfo.objects.create(
            file_path='path2',
            profile='profile2',
            description='test2'
        )

        request = HttpRequest()
        response = index_page(request)

        self.assertIn('path1', response.content.decode('utf-8'))
        self.assertIn('profile1', response.content.decode('utf-8'))
        self.assertIn('test1', response.content.decode('utf-8'))

        self.assertIn('path2', response.content.decode('utf-8'))
        self.assertIn('profile2', response.content.decode('utf-8'))
        self.assertIn('test2', response.content.decode('utf-8'))


class AnalysisViewTest(TestCase):
    def test_analysis_url_resolve(self):
        response = self.client.get('/analysis/1.vmem')

        self.assertTemplateUsed(response, 'analysis.html')


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
