# coding=utf-8
from __future__ import print_function

from os import path

from django.test import LiveServerTestCase
from selenium import webdriver


class FirstUserTest(LiveServerTestCase):
    def setUp(self):
        self.dump_lists = [
            ['/Users/J/Documents/ExampleImage/1.vmem', 'AutoDetect', 'test1'],
            ['/Users/J/Documents/ExampleImage/2.vmem', 'AutoDetect', 'test2'],
            ['asdlfjaldf', 'AutoDetect', 'testalkdfjad']
        ]

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_dump_list(self):
        # 테이블에서 입력된 덤프파일 정보를 확인한다.
        table = self.browser.find_element_by_id('id_dump_list')
        # 테이블 항목 검증
        rows = table.find_elements_by_tag_name('tr')

        for cnt in range(0, len(rows)):
            if cnt == 0:
                self.assertTrue(u'#' in rows[cnt].text)
                self.assertTrue(u'파일 이름' in rows[cnt].text)
                self.assertTrue(u'파일 경로' in rows[cnt].text)
                self.assertTrue(u'프로파일' in rows[cnt].text)
                self.assertTrue(u'설명' in rows[cnt].text)
                continue
            dump = self.dump_lists[cnt - 1]
            tds = rows[cnt].find_elements_by_tag_name('td')
            self.assertEqual(cnt, int(tds[0].text))
            self.assertEqual(path.basename(dump[0]), tds[1].text)
            self.assertEqual(dump[0], tds[2].text)
            self.assertEqual(dump[1], tds[3].text)
            self.assertEqual(dump[2], tds[4].text)

    def add_dump_file(self, file_path, profile, description):
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

    def test_visit_index_page(self):
        # memsys를 처음 사용하는 사용자가 메인 페이지를 방문한다
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더에 'Lyzer'를 표시하고 있다
        self.assertIn(u'Lyzer', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Lyzer', header_text)

        # 분석할 덤프파일을 2회 추가한다
        # 입력내용
        #   메모리 덤프파일 로컬 경로
        #   운영체제 프로파일 정보
        #   덤프파일 설명
        for dump in self.dump_lists:
            # 덤프 파일을 저장한다
            self.add_dump_file(dump[0], dump[1], dump[2])

        # 테이블에서 입력된 덤프 파일을 확인한다
        self.check_for_row_in_dump_list()

        # 테이블에 입력된 정보가 있는지 확인한다
        table = self.browser.find_element_by_id('id_dump_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(len(rows) == len(self.dump_lists) + 1)

        # 테이블에 입력된 항목을 클릭하면 메모리 덤프를 분석할 수 있는
        # 새로운 URL로 바뀐다
        # 첫 번째 항목을 선택한다
        link_text = path.basename(self.dump_lists[1][0])
        link = self.browser.find_element_by_link_text(link_text)
        link.click()
        self.assertRegexpMatches(self.browser.current_url, 'http://localhost:[0-9]*/memsis/analysis/' + link_text)

        # 새로운 기능 테스트 추가하기
        self.fail('Finish the test!')
