from unittest import skip

from django.http import HttpRequest
from django.test import TestCase

# Create your tests here.
from django.urls import resolve

from memsis import views

@skip
class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)


class MainPageTest(TestCase):
    def test_root_url_resolve(self):
        root_url = resolve('/')

        self.assertEqual(root_url.func, views.index)

    def test_returns_correct_main_page(self):
        request = HttpRequest()
        response = views.index(request)

        self.assertTrue(response.content.startswith('<html>'))
        self.assertIn(b'<title>Lyzer</title>', response.content)
        self.assertTrue(response.content.endswith('</html>'))