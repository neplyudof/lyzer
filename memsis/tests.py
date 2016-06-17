from unittest import skip

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from memsis import views
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
        request = HttpRequest()
        request.method = 'POST'
        request.POST['file_path'] = '/Users/J/Documents/ExampleImage/1.vmem'
        request.POST['profile'] = 'AutoDetect'
        request.POST['description'] = 'test'

        response = index_page(request)

        self.assertIn('/Users/J/Documents/ExampleImage/1.vmem', response.content.decode('utf-8'))
        self.assertIn('AutoDetect', response.content.decode('utf-8'))
        self.assertIn('test', response.content.decode('utf-8'))
