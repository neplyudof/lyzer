# coding=utf-8
from __future__ import print_function
import unittest

from selenium import webdriver


class FirstUserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def add_and_check_for_row_in_dump_list(self, file_path, profile, description):
        inputbox = self.browser.find_element_by_id('id_file_path')
        self.assertEqual(inputbox.get_attribute('placeholder'), u'로컬 덤프파일 경로 입력')

        # 로컬 메모리 덤프파일 경로를 입력한다
        inputbox.send_keys(file_path)

        # 운영체제 프로파일을 선택한다
        selectbox = self.browser.find_element_by_id('id_select_profile')
        select_option = selectbox.find_element_by_tag_name('option')
        self.assertEqual(select_option.text, profile)

        # 덤프파일 설명 입력
        textarea = self.browser.find_element_by_id('id_dump_description')
        self.assertEqual(textarea.get_attribute('name'), 'description')
        textarea.send_keys(description)

        # 제출 버튼 클릭으로 페이지가 갱신되며 메모리 덤프 목록에 추가된다
        # 제출 후 추가된 덤프파일 정보를 테이블에서 확인할 수 있다
        submit = self.browser.find_element_by_id('id_dump_submit')
        self.assertEqual(submit.get_attribute('value'), u'추가')
        submit.click()

        # 테이블에서 입력된 덤프파일 정보를 확인한다.
        table = self.browser.find_element_by_id('id_dump_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(file_path in row.text for row in rows))
        self.assertTrue(any(profile in row.text for row in rows))
        self.assertTrue(any(description in row.text for row in rows))

    def test_visit_index_page(self):
        # memsys를 처음 사용하는 사용자가 페이지를 방문한다
        self.browser.get('http://localhost:8080')

        # 웹 페이지 타이틀과 헤더에 'Lyzer'를 표시하고 있다
        self.assertIn(u'Lyzer', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Lyzer', header_text)

        # 테이블 헤드 정보 확인
        table = self.browser.find_element_by_id('id_dump_list')
        ths = table.find_elements_by_tag_name('th')
        self.assertTrue(any(u'파일 경로' == th.text for th in ths))
        self.assertTrue(any(u'프로파일' == th.text for th in ths))
        self.assertTrue(any(u'설명' == th.text for th in ths))

        for th in ths:
            print(th.text)

        # 분석할 덤프파일을 2회 추가한다
        # 입력내용
        #   메모리 덤프파일 로컬 경로
        #   운영체제 프로파일 정보
        #   덤프파일 설명
        self.add_and_check_for_row_in_dump_list('/Users/J/Documents/ExampleImage/1.vmem', 'AutoDetect', u'트로이 목마')
        self.add_and_check_for_row_in_dump_list('/Users/J/Documents/ExampleImage/2.vmem', 'AutoDetect', u'랜섬웨어')

        # 덤프파일을 추가로 입력한다
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
