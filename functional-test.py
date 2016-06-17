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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Lyzer', header_text)

        # 분석할 덤프파일을 추가한다
        # 입력내용
        #   메모리 덤프파일 로컬 경로
        #   운영체제 프로파일 정보
        #   덤프파일 설명
        inputbox = self.browser.find_element_by_id('id_file_path')
        self.assertEqual(inputbox.get_attribute('placeholder'), '로컬 덤프파일 경로 입력')

        # 로컬 메모리 덤프파일 경로를 입력한다
        inputbox.send_keys('/Users/J/Documents/ExampleImage/1.vmem')

        # 운영체제 프로파일을 선택한다
        selectbox = self.browser.find_element_by_id('id_select_profile')
        select_option = selectbox.find_element_by_tag_name('option')
        self.assertEqual(select_option.text, 'AutoDetect')

        # 덤프파일 설명 입력
        textarea = self.browser.find_element_by_id('id_dump_description')
        self.assertEqual(textarea.get_attribute('name'), 'description')
        textarea.send_keys('Test')

        # 제출 버튼 클릭으로 페이지가 갱신되며 메모리 덤프 목록에 추가된다
        submit = self.browser.find_element_by_id('id_dump_submit')
        submit.click()

        table = self.browser.find_element_by_id('id_dump_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('/Users/J/Documents/ExampleImage/1.vmem', any(row for row in rows))

        # 덤프파일을 추가로 입력한다
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
