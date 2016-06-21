# coding=utf-8
from unittest import skip
from urlparse import urlparse

from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
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

    def test_validation_errors_are_sent_back_to_index_page(self):
        response = self.client.post('/', data={'file_path': '', 'profile': 'AutoDetect', 'description': 'test'})
        self.assertEqual(response.status_code, 200)
        expected_error = "This field cannot be blank."
        self.assertContains(response, expected_error)

    def test_invalid_dump_info_arent_saved(self):
        self.client.post('/', data={
            'file_path': '',
            'profile': 'AutoDetect',
            'description': 'test'
        })
        self.assertEqual(DumpInfo.objects.count(), 0)


class AnalysisViewTest(TestCase):
    def test_analysis_url_resolve(self):
        response = self.client.get('/analysis/1.vmem')

        self.assertTemplateUsed(response, 'analysis.html')
