# coding=utf-8
import unittest

from selenium import webdriver


class FirstUserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visit_main_page(self):
        # memsys를 처음 사용하는 사용자가 페이지를 방문한다
        self.browser.get('http://localhost:8080')

        # 웹 페이지 타이틀과 헤더에 'Lyzer'를 표시하고 있다
        self.assertIn(u'Lyzer', self.browser.title)


if __name__ == '__main__':
    unittest.main()
